"""Persistência local de contas NightFall com senhas derivadas por PBKDF2."""

from __future__ import annotations

import os
import re
import secrets
import sqlite3
from pathlib import Path
from typing import TypedDict

from admin_auth import hash_admin_password, verify_admin_password

DEFAULT_AUTH_DB = Path(__file__).with_name("auth_users.sqlite3")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DUMMY_PASSWORD_HASH = hash_admin_password(secrets.token_urlsafe(32))


class Account(TypedDict):
    name: str
    email: str
    cpf: str
    birth_date: str


class AccountAlreadyExists(Exception):
    """O e-mail já pertence a uma conta."""


class AuthStorageError(Exception):
    """A base local de autenticação não pôde ser acessada."""


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def is_valid_email(email: str) -> bool:
    return bool(_EMAIL_PATTERN.fullmatch(normalize_email(email)))


def _connect(db_path: Path | None = None) -> sqlite3.Connection:
    configured_path = db_path or os.getenv("NIGHTFALL_AUTH_DB") or DEFAULT_AUTH_DB
    path = Path(configured_path)
    connection = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                cpf TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        return connection
    except (OSError, sqlite3.Error) as exc:
        if connection is not None:
            connection.close()
        raise AuthStorageError("Não foi possível abrir o banco de autenticação.") from exc


def create_account(
    *,
    name: str,
    email: str,
    cpf: str,
    birth_date: str,
    password: str,
    db_path: Path | None = None,
) -> Account:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise ValueError("Informe um e-mail válido.")
    if len(password) < 8:
        raise ValueError("A senha deve conter pelo menos 8 caracteres.")

    password_hash = hash_admin_password(password)
    connection = _connect(db_path)
    try:
        with connection:
            connection.execute(
                """
                INSERT INTO users (name, email, cpf, birth_date, password_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name.strip(), normalized_email, cpf, birth_date.strip(), password_hash),
            )
    except sqlite3.IntegrityError as exc:
        raise AccountAlreadyExists from exc
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível salvar a conta.") from exc
    finally:
        connection.close()

    return {
        "name": name.strip(),
        "email": normalized_email,
        "cpf": cpf,
        "birth_date": birth_date.strip(),
    }


def authenticate_account(
    email: str,
    password: str,
    *,
    db_path: Path | None = None,
) -> Account | None:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email) or not password:
        verify_admin_password(password or "", _DUMMY_PASSWORD_HASH)
        return None

    connection = _connect(db_path)
    try:
        row = connection.execute(
            """
            SELECT name, email, cpf, birth_date, password_hash
            FROM users
            WHERE email = ?
            """,
            (normalized_email,),
        ).fetchone()
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível consultar o banco de autenticação.") from exc
    finally:
        connection.close()

    password_hash = row["password_hash"] if row is not None else _DUMMY_PASSWORD_HASH
    password_matches = verify_admin_password(password, password_hash)
    if row is None or not password_matches:
        return None

    return {
        "name": row["name"],
        "email": row["email"],
        "cpf": row["cpf"],
        "birth_date": row["birth_date"],
    }
