import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch

from app import chat, database


class ChatServiceTests(unittest.TestCase):
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

    def tearDown(self) -> None:
        self.environment.stop()
        self.temp_dir.cleanup()

    def test_create_user_returns_group_identity(self) -> None:
        user = chat.create_user("ana")

        self.assertEqual(user, {"username": "ana", "identity": "ana@g1"})

    def test_duplicate_user_is_rejected(self) -> None:
        chat.create_user("ana")

        with self.assertRaises(chat.UserAlreadyExistsError):
            chat.create_user("ANA")

    def test_messages_are_ordered_and_use_incrementing_lamport_clock(self) -> None:
        chat.create_user("ana")
        first = chat.send_message("ana", "Hola")
        second = chat.send_message("ana", "¿Cómo están?")

        self.assertEqual(first["from"], "ana@g1")
        self.assertEqual(first["lamport"], 1)
        self.assertEqual(second["lamport"], 2)
        self.assertEqual(
            [message["id"] for message in chat.get_messages()],
            [first["id"], second["id"]],
        )

    def test_messages_and_users_survive_database_reinitialization(self) -> None:
        chat.create_user("ana")
        sent = chat.send_message("ana", "Mensaje guardado")

        database.init_db()

        messages = chat.get_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["id"], sent["id"])
        self.assertEqual(messages[0]["body"], "Mensaje guardado")


class DatabaseMigrationTests(unittest.TestCase):
    def test_existing_local_messages_migrate_for_federated_messages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "chat.sqlite3")
            with patch.dict(
                os.environ,
                {"CHAT_DB_PATH": database_path, "GROUP_ID": "g1"},
            ):
                with closing(sqlite3.connect(database_path)) as connection, connection:
                    connection.executescript(
                        """
                        CREATE TABLE users (
                            username TEXT PRIMARY KEY COLLATE NOCASE,
                            created_at TEXT NOT NULL
                        );
                        CREATE TABLE server_state (
                            id INTEGER PRIMARY KEY CHECK (id = 1),
                            lamport_clock INTEGER NOT NULL
                        );
                        INSERT INTO server_state (id, lamport_clock) VALUES (1, 1);
                        CREATE TABLE messages (
                            id TEXT PRIMARY KEY,
                            username TEXT NOT NULL COLLATE NOCASE,
                            sender TEXT NOT NULL,
                            origin TEXT NOT NULL,
                            lamport INTEGER NOT NULL,
                            sent_at TEXT NOT NULL,
                            body TEXT NOT NULL,
                            FOREIGN KEY (username) REFERENCES users(username)
                        );
                        CREATE INDEX idx_messages_order
                        ON messages (lamport, origin, id);
                        INSERT INTO users (username, created_at)
                        VALUES ('ana', '2026-11-08T12:00:00+00:00');
                        INSERT INTO messages
                            (id, username, sender, origin, lamport, sent_at, body)
                        VALUES (
                            'local-1',
                            'ana',
                            'ana@g1',
                            'g1',
                            1,
                            '2026-11-08T12:00:00+00:00',
                            'Mensaje anterior'
                        );
                        """
                    )
                database.init_db()
                messages = database.list_messages()
                incoming_message = {
                    "id": "remote-1",
                    "from": "luz@g2",
                    "origin": "g2",
                    "lamport": 2,
                    "sent_at": "2026-11-08T12:00:01+00:00",
                    "body": "Mensaje remoto",
                }

                self.assertEqual(messages[0]["id"], "local-1")
                self.assertTrue(database.insert_incoming_message(incoming_message))
                self.assertEqual(len(database.list_messages()), 2)
