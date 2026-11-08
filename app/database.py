import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

Message = dict[str, str | int]


def _database_path() -> Path:
    return Path(os.getenv("CHAT_DB_PATH", "data/chat.sqlite3")).expanduser()


@contextmanager
def _connection() -> Generator[sqlite3.Connection, None, None]:
    path = _database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    finally:
        connection.close()


def _create_message_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE messages (
            id TEXT PRIMARY KEY,
            username TEXT COLLATE NOCASE,
            sender TEXT NOT NULL,
            origin TEXT NOT NULL,
            lamport INTEGER NOT NULL,
            sent_at TEXT NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
        """
    )


def _migrate_messages(connection: sqlite3.Connection) -> None:
    columns = connection.execute("PRAGMA table_info(messages)").fetchall()
    if not columns:
        _create_message_table(connection)
        return

    username_column = next(
        (column for column in columns if column["name"] == "username"),
        None,
    )
    if username_column is None:
        raise RuntimeError("The messages table has an unsupported schema")
    if not username_column["notnull"]:
        return

    connection.execute("DROP INDEX IF EXISTS idx_messages_order")
    connection.execute("ALTER TABLE messages RENAME TO messages_legacy")
    _create_message_table(connection)
    connection.execute(
        """
        INSERT INTO messages (id, username, sender, origin, lamport, sent_at, body)
        SELECT id, username, sender, origin, lamport, sent_at, body
        FROM messages_legacy
        """
    )
    connection.execute("DROP TABLE messages_legacy")


def init_db() -> None:
    with _connection() as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY COLLATE NOCASE,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS server_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                lamport_clock INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO server_state (id, lamport_clock) VALUES (1, 0)"
        )
        _migrate_messages(connection)
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_messages_order
            ON messages (lamport, origin, id)
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS outbox (
                message_id TEXT PRIMARY KEY,
                attempts INTEGER NOT NULL DEFAULT 0,
                next_attempt_at TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                event_type TEXT NOT NULL,
                message_id TEXT,
                lamport INTEGER,
                detail TEXT NOT NULL
            )
            """
        )
        connection.commit()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _record_event(
    connection: sqlite3.Connection,
    *,
    event_type: str,
    message_id: str | None,
    lamport: int | None,
    detail: str,
) -> None:
    connection.execute(
        """
        INSERT INTO event_log (created_at, event_type, message_id, lamport, detail)
        VALUES (?, ?, ?, ?, ?)
        """,
        (_utc_now(), event_type, message_id, lamport, detail),
    )


def record_event(
    *,
    event_type: str,
    message_id: str | None = None,
    lamport: int | None = None,
    detail: str,
) -> None:
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        _record_event(
            connection,
            event_type=event_type,
            message_id=message_id,
            lamport=lamport,
            detail=detail,
        )
        connection.commit()


def create_user_record(username: str, created_at: str) -> None:
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO users (username, created_at) VALUES (?, ?)",
            (username, created_at),
        )
        connection.commit()


def user_exists(username: str) -> bool:
    with _connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return row is not None


def _user_exists_in_connection(
    connection: sqlite3.Connection,
    username: str,
) -> bool:
    row = connection.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    return row is not None


def _current_lamport(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        "SELECT lamport_clock FROM server_state WHERE id = 1"
    ).fetchone()
    if row is None:
        raise RuntimeError("Server clock state is missing")
    return int(row["lamport_clock"])


def save_local_message(
    *,
    message_id: str,
    username: str,
    sender: str,
    origin: str,
    sent_at: str,
    body: str,
) -> Message:
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        if not _user_exists_in_connection(connection, username):
            connection.rollback()
            raise LookupError(username)

        connection.execute(
            "UPDATE server_state SET lamport_clock = lamport_clock + 1 WHERE id = 1"
        )
        lamport = _current_lamport(connection)
        connection.execute(
            """
            INSERT INTO messages
                (id, username, sender, origin, lamport, sent_at, body)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (message_id, username, sender, origin, lamport, sent_at, body),
        )
        connection.execute(
            "INSERT INTO outbox (message_id, next_attempt_at) VALUES (?, ?)",
            (message_id, sent_at),
        )
        _record_event(
            connection,
            event_type="message.queued",
            message_id=message_id,
            lamport=lamport,
            detail=f"Mensaje local de {sender} pendiente de envío al central",
        )
        connection.commit()

    return {
        "id": message_id,
        "from": sender,
        "origin": origin,
        "lamport": lamport,
        "sent_at": sent_at,
        "body": body,
    }


def insert_incoming_message(message: dict[str, str | int]) -> bool:
    message_id = str(message["id"])
    sender = str(message["from"])
    origin = str(message["origin"])
    received_lamport = int(message["lamport"])
    sent_at = str(message["sent_at"])
    body = str(message["body"])

    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        exists = connection.execute(
            "SELECT 1 FROM messages WHERE id = ?",
            (message_id,),
        ).fetchone()
        if exists is not None:
            connection.rollback()
            return False

        connection.execute(
            """
            UPDATE server_state
            SET lamport_clock = MAX(lamport_clock, ?) + 1
            WHERE id = 1
            """,
            (received_lamport,),
        )
        local_lamport = _current_lamport(connection)
        connection.execute(
            """
            INSERT INTO messages
                (id, username, sender, origin, lamport, sent_at, body)
            VALUES (?, NULL, ?, ?, ?, ?, ?)
            """,
            (
                message_id,
                sender,
                origin,
                received_lamport,
                sent_at,
                body,
            ),
        )
        _record_event(
            connection,
            event_type="message.received",
            message_id=message_id,
            lamport=received_lamport,
            detail=f"Mensaje recibido de {sender}; reloj local actualizado a {local_lamport}",
        )
        connection.commit()
    return True


def get_lamport_clock() -> int:
    with _connection() as connection:
        return _current_lamport(connection)


def list_messages() -> list[Message]:
    with _connection() as connection:
        rows = connection.execute(
            """
            SELECT id, sender, origin, lamport, sent_at, body
            FROM messages
            ORDER BY lamport, origin, id
            """
        ).fetchall()
    return [
        {
            "id": row["id"],
            "from": row["sender"],
            "origin": row["origin"],
            "lamport": int(row["lamport"]),
            "sent_at": row["sent_at"],
            "body": row["body"],
        }
        for row in rows
    ]


def get_next_pending_message() -> tuple[Message, int] | None:
    now = _utc_now()
    with _connection() as connection:
        row = connection.execute(
            """
            SELECT m.id, m.sender, m.origin, m.lamport, m.sent_at, m.body,
                   o.attempts
            FROM outbox AS o
            JOIN messages AS m ON m.id = o.message_id
            WHERE o.next_attempt_at <= ?
            ORDER BY o.next_attempt_at, m.lamport, m.id
            LIMIT 1
            """,
            (now,),
        ).fetchone()
    if row is None:
        return None

    return (
        {
            "id": row["id"],
            "from": row["sender"],
            "origin": row["origin"],
            "lamport": int(row["lamport"]),
            "sent_at": row["sent_at"],
            "body": row["body"],
        },
        int(row["attempts"]),
    )


def mark_message_delivered(message_id: str, lamport: int) -> None:
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DELETE FROM outbox WHERE message_id = ?", (message_id,))
        _record_event(
            connection,
            event_type="message.sent",
            message_id=message_id,
            lamport=lamport,
            detail="Mensaje aceptado por el servidor central",
        )
        connection.commit()


def schedule_message_retry(
    *,
    message_id: str,
    lamport: int,
    attempts: int,
    delay_seconds: int,
    detail: str,
) -> None:
    next_attempt = datetime.now(timezone.utc).timestamp() + delay_seconds
    next_attempt_at = datetime.fromtimestamp(
        next_attempt,
        tz=timezone.utc,
    ).isoformat(timespec="milliseconds")
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            """
            UPDATE outbox
            SET attempts = ?, next_attempt_at = ?
            WHERE message_id = ?
            """,
            (attempts, next_attempt_at, message_id),
        )
        _record_event(
            connection,
            event_type="message.retry",
            message_id=message_id,
            lamport=lamport,
            detail=f"Reintento {attempts} en {delay_seconds}s: {detail}",
        )
        connection.commit()


def discard_message(message_id: str, lamport: int, detail: str) -> None:
    with _connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DELETE FROM outbox WHERE message_id = ?", (message_id,))
        _record_event(
            connection,
            event_type="message.discarded",
            message_id=message_id,
            lamport=lamport,
            detail=detail,
        )
        connection.commit()


def list_events(limit: int = 100) -> list[dict[str, str | int | None]]:
    with _connection() as connection:
        rows = connection.execute(
            """
            SELECT created_at, event_type, message_id, lamport, detail
            FROM event_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [
        {
            "created_at": row["created_at"],
            "event_type": row["event_type"],
            "message_id": row["message_id"],
            "lamport": row["lamport"],
            "detail": row["detail"],
        }
        for row in rows
    ]
