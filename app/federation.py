import asyncio
import logging
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator
from urllib.parse import urlparse

import httpx
from pydantic import ValidationError

from app import database
from app.schemas import FederatedMessage

logger = logging.getLogger("chat.federation")


def get_group_id() -> str:
    return os.getenv("GROUP_ID", "g1").strip()


@dataclass(frozen=True)
class FederationSettings:
    group_id: str
    central_url: str
    public_url: str
    health_interval_seconds: int
    health_failure_threshold: int
    registration_interval_seconds: int
    retry_initial_seconds: int
    retry_max_seconds: int

    @classmethod
    def from_environment(cls) -> FederationSettings | None:
        central_url = os.getenv("CENTRAL_URL", "").strip().rstrip("/")
        if not central_url:
            return None

        parsed_url = urlparse(central_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("CENTRAL_URL debe ser una URL HTTP o HTTPS válida.")

        public_url = os.getenv("PUBLIC_URL", "").strip().rstrip("/")
        if not public_url:
            raise ValueError(
                "PUBLIC_URL es obligatorio cuando CENTRAL_URL está configurado."
            )
        parsed_public_url = urlparse(public_url)
        if parsed_public_url.scheme not in {"http", "https"} or not parsed_public_url.netloc:
            raise ValueError("PUBLIC_URL debe ser una URL HTTP o HTTPS válida.")

        retry_initial_seconds = _positive_int("RETRY_INITIAL_SECONDS", 1)
        retry_max_seconds = _positive_int("RETRY_MAX_SECONDS", 30)
        if retry_max_seconds < retry_initial_seconds:
            raise ValueError(
                "RETRY_MAX_SECONDS no puede ser menor que RETRY_INITIAL_SECONDS."
            )

        return cls(
            group_id=get_group_id(),
            central_url=central_url,
            public_url=public_url,
            health_interval_seconds=_positive_int("HEALTH_INTERVAL_SECONDS", 5),
            health_failure_threshold=_positive_int(
                "HEALTH_FAILURE_THRESHOLD",
                3,
            ),
            registration_interval_seconds=_positive_int(
                "REGISTRATION_INTERVAL_SECONDS",
                30,
            ),
            retry_initial_seconds=retry_initial_seconds,
            retry_max_seconds=retry_max_seconds,
        )


def _positive_int(name: str, default: int) -> int:
    value = os.getenv(name)
    try:
        parsed = default if value is None or value == "" else int(value)
    except ValueError as exc:
        raise ValueError(f"{name} debe ser un número entero positivo.") from exc
    if parsed < 1:
        raise ValueError(f"{name} debe ser un número entero positivo.")
    return parsed


def retry_delay(attempt: int, initial_seconds: int, max_seconds: int) -> int:
    if attempt < 1:
        raise ValueError("El número de intento debe ser positivo.")
    if initial_seconds < 1 or max_seconds < initial_seconds:
        raise ValueError("La configuración de espera exponencial no es válida.")
    return min(initial_seconds * (2 ** (attempt - 1)), max_seconds)


def _require_successful_response(response: httpx.Response) -> None:
    if not response.is_success:
        raise httpx.HTTPStatusError(
            f"Unexpected HTTP status {response.status_code}",
            request=response.request,
            response=response,
        )


async def sync_history(client: httpx.AsyncClient) -> int:
    since = database.get_lamport_clock()
    response = await client.get("/history", params={"since": since})
    _require_successful_response(response)
    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError(
            "La respuesta provisional de GET /history debe ser una lista JSON."
        )

    received_count = 0
    for item in payload:
        message = FederatedMessage.model_validate(item)
        stored = database.insert_incoming_message(
            {
                "id": message.id,
                "from": message.sender,
                "origin": message.origin,
                "lamport": message.lamport,
                "sent_at": message.sent_at,
                "body": message.body,
            }
        )
        if stored:
            received_count += 1
            logger.info(
                "Mensaje recuperado id=%s lamport=%s desde=%s",
                message.id,
                message.lamport,
                message.sender,
            )
    database.record_event(
        event_type="history.recovered",
        detail=(
            f"GET /history?since={since}: "
            f"{received_count} mensaje(s) nuevo(s)"
        ),
    )
    return received_count


async def _registration_loop(
    client: httpx.AsyncClient,
    settings: FederationSettings,
) -> None:
    while True:
        await register_once(client, settings)
        await asyncio.sleep(settings.registration_interval_seconds)


async def register_once(
    client: httpx.AsyncClient,
    settings: FederationSettings,
) -> bool:
    try:
        response = await client.post(
            "/register",
            json={
                "server": settings.group_id,
                "url": settings.public_url,
            },
        )
        _require_successful_response(response)
    except httpx.RequestError as exc:
        detail = f"No se pudo registrar {settings.group_id}: {exc}"
        logger.error(detail)
        database.record_event(event_type="registration.failed", detail=detail)
        return False
    except httpx.HTTPStatusError as exc:
        detail = (
            f"El registro de {settings.group_id} respondió "
            f"HTTP {exc.response.status_code}"
        )
        logger.error(detail)
        database.record_event(event_type="registration.failed", detail=detail)
        return False

    logger.info(
        "Servidor registrado server=%s url=%s",
        settings.group_id,
        settings.public_url,
    )
    database.record_event(
        event_type="registration.succeeded",
        detail=f"Servidor registrado como {settings.group_id}",
    )
    return True


async def _health_loop(
    client: httpx.AsyncClient,
    settings: FederationSettings,
) -> None:
    consecutive_failures = 0
    central_is_down = False
    history_is_synced = False

    while True:
        try:
            response = await client.get("/health")
            _require_successful_response(response)
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            consecutive_failures += 1
            history_is_synced = False
            logger.warning(
                "Health del central falló (%s/%s): %s",
                consecutive_failures,
                settings.health_failure_threshold,
                exc,
            )
            if (
                consecutive_failures >= settings.health_failure_threshold
                and not central_is_down
            ):
                central_is_down = True
                detail = (
                    "Central marcado como caído después de "
                    f"{consecutive_failures} fallos de health"
                )
                logger.error(detail)
                database.record_event(
                    event_type="central.down",
                    detail=detail,
                )
        else:
            consecutive_failures = 0
            if central_is_down:
                central_is_down = False
                detail = "El servidor central volvió a responder"
                logger.info(detail)
                database.record_event(
                    event_type="central.recovered",
                    detail=detail,
                )

            if not history_is_synced:
                try:
                    recovered_count = await sync_history(client)
                except (
                    httpx.RequestError,
                    httpx.HTTPStatusError,
                    ValueError,
                    ValidationError,
                ) as exc:
                    logger.error("No se pudo recuperar el historial: %s", exc)
                    database.record_event(
                        event_type="history.failed",
                        detail=str(exc),
                    )
                else:
                    history_is_synced = True
                    logger.info(
                        "Recuperación de historial finalizada; mensajes nuevos=%s",
                        recovered_count,
                    )
        await asyncio.sleep(settings.health_interval_seconds)


async def deliver_pending_once(
    client: httpx.AsyncClient,
    settings: FederationSettings,
) -> bool:
    pending = database.get_next_pending_message()
    if pending is None:
        return False

    message, previous_attempts = pending
    message_id = str(message["id"])
    lamport = int(message["lamport"])
    try:
        response = await client.post("/messages", json=message)
    except httpx.RequestError as exc:
        attempt = previous_attempts + 1
        delay = retry_delay(
            attempt,
            settings.retry_initial_seconds,
            settings.retry_max_seconds,
        )
        database.schedule_message_retry(
            message_id=message_id,
            lamport=lamport,
            attempts=attempt,
            delay_seconds=delay,
            detail=str(exc),
        )
        logger.warning(
            "Reintento programado id=%s lamport=%s intento=%s espera=%ss error=%s",
            message_id,
            lamport,
            attempt,
            delay,
            exc,
        )
    else:
        if 400 <= response.status_code < 500:
            detail = (
                f"El central descartó el mensaje con HTTP "
                f"{response.status_code}"
            )
            database.discard_message(message_id, lamport, detail)
            logger.error(
                "Mensaje descartado id=%s lamport=%s status=%s",
                message_id,
                lamport,
                response.status_code,
            )
        elif not response.is_success:
            attempt = previous_attempts + 1
            delay = retry_delay(
                attempt,
                settings.retry_initial_seconds,
                settings.retry_max_seconds,
            )
            detail = f"El central respondió HTTP {response.status_code}"
            database.schedule_message_retry(
                message_id=message_id,
                lamport=lamport,
                attempts=attempt,
                delay_seconds=delay,
                detail=detail,
            )
            logger.warning(
                "Reintento programado id=%s lamport=%s intento=%s espera=%ss status=%s",
                message_id,
                lamport,
                attempt,
                delay,
                response.status_code,
            )
        else:
            database.mark_message_delivered(message_id, lamport)
            logger.info(
                "Mensaje enviado id=%s lamport=%s status=%s",
                message_id,
                lamport,
                response.status_code,
            )
    return True


async def _outbox_loop(
    client: httpx.AsyncClient,
    settings: FederationSettings,
) -> None:
    while True:
        had_message = await deliver_pending_once(client, settings)
        if not had_message:
            await asyncio.sleep(0.5)


@asynccontextmanager
async def run_federation(
    settings: FederationSettings,
) -> AsyncGenerator[None, None]:
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(
        base_url=settings.central_url,
        timeout=timeout,
    ) as client:
        tasks = [
            asyncio.create_task(_registration_loop(client, settings)),
            asyncio.create_task(_health_loop(client, settings)),
            asyncio.create_task(_outbox_loop(client, settings)),
        ]
        try:
            yield
        finally:
            for task in tasks:
                task.cancel()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, BaseException) and not isinstance(
                    result,
                    asyncio.CancelledError,
                ):
                    raise result
