import os
import re
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from app import database

_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")


class UserAlreadyExistsError(Exception):
    pass


class UnknownUserError(Exception):
    pass


class InvalidUsernameError(Exception):
    pass


def _group_id() -> str:
    return os.getenv("GROUP_ID", "g1")


def _validate_username(username: str) -> str:
    cleaned = username.strip()
    if not _USERNAME_PATTERN.fullmatch(cleaned):
        raise InvalidUsernameError(
            "El nombre debe tener entre 1 y 32 caracteres: letras, números, punto, guion o guion bajo."
        )
    return cleaned


def create_user(username: str) -> dict[str, str]:
    cleaned = _validate_username(username)
    created_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    try:
        database.create_user_record(cleaned, created_at)
    except sqlite3.IntegrityError as exc:
        raise UserAlreadyExistsError(cleaned) from exc

    return {
        "username": cleaned,
        "identity": f"{cleaned}@{_group_id()}",
    }


def send_message(username: str, body: str) -> dict[str, str | int]:
    cleaned = _validate_username(username)
    if not database.user_exists(cleaned):
        raise UnknownUserError(cleaned)

    sent_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    sender = f"{cleaned}@{_group_id()}"
    try:
        return database.save_local_message(
            message_id=str(uuid4()),
            username=cleaned,
            sender=sender,
            origin=_group_id(),
            sent_at=sent_at,
            body=body.strip(),
        )
    except LookupError as exc:
        raise UnknownUserError(cleaned) from exc


def get_messages() -> list[dict[str, str | int]]:
    return database.list_messages()
