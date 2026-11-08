import asyncio
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import httpx

from app import chat, database
from app.federation import (
    FederationSettings,
    deliver_pending_once,
    register_once,
    retry_delay,
    sync_history,
)
from app.main import app


class FederationRouteTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.environment = patch.dict(
            os.environ,
            {
                "CHAT_DB_PATH": os.path.join(self.temp_dir.name, "chat.sqlite3"),
                "GROUP_ID": "g1",
                "CENTRAL_URL": "",
                "PUBLIC_URL": "",
            },
        )
        self.environment.start()
        self.lifespan = app.router.lifespan_context(app)
        await self.lifespan.__aenter__()
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()
        await self.lifespan.__aexit__(None, None, None)
        self.environment.stop()
        self.temp_dir.cleanup()

    async def test_federation_health_returns_group_and_lamport_clock(self) -> None:
        response = await self.client.get("/fed/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"server": "g1", "lamport": 0})

    async def test_incoming_message_is_persisted_and_deduplicated(self) -> None:
        message = {
            "id": "message-123",
            "from": "ana@g2",
            "origin": "g2",
            "lamport": 42,
            "sent_at": "2026-11-08T12:00:00Z",
            "body": "Hola desde otro grupo",
            "unknown_extension": "ignored",
        }

        first_response = await self.client.post("/fed/messages", json=message)
        first_health = (await self.client.get("/fed/health")).json()
        second_response = await self.client.post("/fed/messages", json=message)
        second_health = (await self.client.get("/fed/health")).json()

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(first_health["lamport"], 43)
        self.assertEqual(second_health["lamport"], 43)
        self.assertEqual(len((await self.client.get("/messages")).json()), 1)


class FederationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.environment = patch.dict(
            os.environ,
            {
                "CHAT_DB_PATH": os.path.join(self.temp_dir.name, "chat.sqlite3"),
                "GROUP_ID": "g1",
            },
        )
        self.environment.start()
        database.init_db()
        self.settings = FederationSettings(
            group_id="g1",
            central_url="http://central.test",
            public_url="https://g1.example.test",
            health_interval_seconds=5,
            health_failure_threshold=3,
            registration_interval_seconds=30,
            retry_initial_seconds=1,
            retry_max_seconds=30,
        )

    def tearDown(self) -> None:
        self.environment.stop()
        self.temp_dir.cleanup()

    def test_retry_delay_grows_exponentially_and_is_capped(self) -> None:
        delays = [
            retry_delay(attempt, initial_seconds=1, max_seconds=30)
            for attempt in range(1, 7)
        ]

        self.assertEqual(delays, [1, 2, 4, 8, 16, 30])

    def test_registration_uses_pdf_fields(self) -> None:
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200)

        async def run() -> bool:
            transport = httpx.MockTransport(handler)
            async with httpx.AsyncClient(
                base_url=self.settings.central_url,
                transport=transport,
            ) as client:
                return await register_once(client, self.settings)

        self.assertTrue(asyncio.run(run()))
        self.assertEqual(requests[0].url.path, "/register")
        self.assertEqual(
            json.loads(requests[0].read()),
            {"server": "g1", "url": "https://g1.example.test"},
        )

    def test_successful_send_removes_message_from_outbox(self) -> None:
        chat.create_user("ana")
        message = chat.send_message("ana", "Envío de prueba")

        def handler(_: httpx.Request) -> httpx.Response:
            return httpx.Response(200)

        async def run() -> bool:
            transport = httpx.MockTransport(handler)
            async with httpx.AsyncClient(
                base_url=self.settings.central_url,
                transport=transport,
            ) as client:
                return await deliver_pending_once(client, self.settings)

        self.assertTrue(asyncio.run(run()))
        self.assertIsNone(database.get_next_pending_message())
        self.assertIn(
            message["id"],
            [event["message_id"] for event in database.list_events()],
        )

    def test_server_error_schedules_retry_and_keeps_message(self) -> None:
        chat.create_user("ana")
        message = chat.send_message("ana", "Reintento de prueba")

        def handler(_: httpx.Request) -> httpx.Response:
            return httpx.Response(503)

        async def run() -> bool:
            transport = httpx.MockTransport(handler)
            async with httpx.AsyncClient(
                base_url=self.settings.central_url,
                transport=transport,
            ) as client:
                return await deliver_pending_once(client, self.settings)

        self.assertTrue(asyncio.run(run()))
        self.assertIsNone(database.get_next_pending_message())
        events = database.list_events()
        self.assertTrue(
            any(
                event["event_type"] == "message.retry"
                and event["message_id"] == message["id"]
                for event in events
            )
        )

    def test_client_error_discards_outbox_entry(self) -> None:
        chat.create_user("ana")
        message = chat.send_message("ana", "Mensaje rechazado")

        def handler(_: httpx.Request) -> httpx.Response:
            return httpx.Response(400)

        async def run() -> bool:
            transport = httpx.MockTransport(handler)
            async with httpx.AsyncClient(
                base_url=self.settings.central_url,
                transport=transport,
            ) as client:
                return await deliver_pending_once(client, self.settings)

        self.assertTrue(asyncio.run(run()))
        self.assertIsNone(database.get_next_pending_message())
        events = database.list_events()
        self.assertTrue(
            any(
                event["event_type"] == "message.discarded"
                and event["message_id"] == message["id"]
                for event in events
            )
        )

    def test_history_recovery_parses_list_and_updates_lamport(self) -> None:
        received = {
            "id": "history-1",
            "from": "ana@g2",
            "origin": "g2",
            "lamport": 42,
            "sent_at": "2026-11-08T12:00:00Z",
            "body": "Recuperado",
        }
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, json=[received])

        async def run() -> tuple[int, int]:
            transport = httpx.MockTransport(handler)
            async with httpx.AsyncClient(
                base_url=self.settings.central_url,
                transport=transport,
            ) as client:
                count = await sync_history(client)
                return count, database.get_lamport_clock()

        recovered_count, lamport = asyncio.run(run())

        self.assertEqual(recovered_count, 1)
        self.assertEqual(lamport, 43)
        self.assertEqual(len(database.list_messages()), 1)
        self.assertEqual(requests[0].url.params["since"], "0")
