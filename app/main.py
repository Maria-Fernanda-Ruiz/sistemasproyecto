import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app import chat, database, federation
from app.schemas import (
    FederatedMessage,
    MessageCreate,
    MessageResponse,
    UserCreate,
    UserResponse,
)

STATIC_DIR = Path(__file__).parent / "static"
logger = logging.getLogger("chat.server")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    database.init_db()
    settings = federation.FederationSettings.from_environment()
    if settings is None:
        logger.warning(
            "CENTRAL_URL no está configurado; el servidor opera en modo local."
        )
        yield
        return

    async with federation.run_federation(settings):
        yield


app = FastAPI(title="Chat distribuido - servidor local", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(payload: UserCreate) -> UserResponse:
    try:
        return chat.create_user(payload.username)
    except chat.InvalidUsernameError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except chat.UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ese nombre de usuario ya existe. Elige otro.",
        ) from exc


@app.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_message(payload: MessageCreate) -> MessageResponse:
    try:
        return chat.send_message(payload.username, payload.body)
    except chat.InvalidUsernameError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except chat.UnknownUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe ese usuario local. Regístralo de nuevo.",
        ) from exc


@app.get("/messages", response_model=list[MessageResponse])
def read_messages() -> list[MessageResponse]:
    return chat.get_messages()


@app.get("/fed/health")
def federation_health() -> dict[str, str | int]:
    return {
        "server": federation.get_group_id(),
        "lamport": database.get_lamport_clock(),
    }


@app.post("/fed/messages", status_code=status.HTTP_200_OK)
def receive_federated_message(payload: FederatedMessage) -> Response:
    message = {
        "id": payload.id,
        "from": payload.sender,
        "origin": payload.origin,
        "lamport": payload.lamport,
        "sent_at": payload.sent_at,
        "body": payload.body,
    }
    inserted = database.insert_incoming_message(message)
    if inserted:
        logger.info(
            "Mensaje federado recibido id=%s lamport=%s desde=%s",
            payload.id,
            payload.lamport,
            payload.sender,
        )
    else:
        logger.info(
            "Mensaje duplicado reconocido id=%s; sin efectos",
            payload.id,
        )
    return Response(status_code=status.HTTP_200_OK)
