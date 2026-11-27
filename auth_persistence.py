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


class SavedAddress(TypedDict):
    id: str
    title: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    cep: str
    is_main: bool


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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                email TEXT PRIMARY KEY COLLATE NOCASE,
                name TEXT NOT NULL DEFAULT '',
                cpf TEXT NOT NULL DEFAULT '',
                birth_date TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO profiles (email, name, cpf, birth_date)
            SELECT email, name, cpf, birth_date FROM users
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses (
                id TEXT PRIMARY KEY,
                owner_email TEXT NOT NULL COLLATE NOCASE,
                title TEXT NOT NULL,
                street TEXT NOT NULL,
                number TEXT NOT NULL,
                complement TEXT NOT NULL DEFAULT '',
                neighborhood TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                cep TEXT NOT NULL,
                is_main INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS addresses_owner_idx ON addresses(owner_email, created_at)"
        )
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS one_main_address_per_owner
            ON addresses(owner_email) WHERE is_main = 1
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
            connection.execute(
                """
                INSERT INTO profiles (email, name, cpf, birth_date)
                VALUES (?, ?, ?, ?)
                """,
                (normalized_email, name.strip(), cpf, birth_date.strip()),
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


def load_profile(email: str, *, db_path: Path | None = None) -> Account | None:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        return None

    connection = _connect(db_path)
    try:
        row = connection.execute(
            "SELECT email, name, cpf, birth_date FROM profiles WHERE email = ?",
            (normalized_email,),
        ).fetchone()
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível consultar os dados do perfil.") from exc
    finally:
        connection.close()

    if row is None:
        return None
    return {
        "name": row["name"],
        "email": row["email"],
        "cpf": row["cpf"],
        "birth_date": row["birth_date"],
    }


def save_profile(
    email: str,
    *,
    name: str,
    cpf: str,
    birth_date: str,
    db_path: Path | None = None,
) -> Account:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise ValueError("O e-mail do perfil é inválido.")
    if not name.strip():
        raise ValueError("O nome não pode ficar vazio.")

    profile = (name.strip(), cpf.strip(), birth_date.strip())
    connection = _connect(db_path)
    try:
        with connection:
            connection.execute(
                """
                INSERT INTO profiles (email, name, cpf, birth_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    name = excluded.name,
                    cpf = excluded.cpf,
                    birth_date = excluded.birth_date,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (normalized_email, *profile),
            )
            connection.execute(
                """
                UPDATE users
                SET name = ?, cpf = ?, birth_date = ?
                WHERE email = ?
                """,
                (*profile, normalized_email),
            )
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível salvar os dados do perfil.") from exc
    finally:
        connection.close()

    return {
        "name": profile[0],
        "email": normalized_email,
        "cpf": profile[1],
        "birth_date": profile[2],
    }


def load_addresses(email: str, *, db_path: Path | None = None) -> list[SavedAddress]:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        return []

    connection = _connect(db_path)
    try:
        rows = connection.execute(
            """
            SELECT id, title, street, number, complement, neighborhood,
                   city, state, cep, is_main
            FROM addresses
            WHERE owner_email = ?
            ORDER BY is_main DESC, created_at, id
            """,
            (normalized_email,),
        ).fetchall()
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível carregar os endereços.") from exc
    finally:
        connection.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "street": row["street"],
            "number": row["number"],
            "complement": row["complement"],
            "neighborhood": row["neighborhood"],
            "city": row["city"],
            "state": row["state"],
            "cep": row["cep"],
            "is_main": bool(row["is_main"]),
        }
        for row in rows
    ]


def save_address(
    email: str,
    *,
    title: str,
    street: str,
    number: str,
    complement: str,
    neighborhood: str,
    city: str,
    state: str,
    cep: str,
    db_path: Path | None = None,
    deduplicate: bool = False,
) -> SavedAddress:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise ValueError("O e-mail do perfil é inválido.")

    address = {
        "title": title.strip() or "Endereço",
        "street": street.strip(),
        "number": number.strip(),
        "complement": complement.strip(),
        "neighborhood": neighborhood.strip(),
        "city": city.strip(),
        "state": state.strip().upper(),
        "cep": "".join(filter(str.isdigit, cep))[:8],
    }
    if not all(address[key] for key in ("street", "number", "city", "state")):
        raise ValueError("Preencha logradouro, número, cidade e estado.")
    if len(address["cep"]) != 8 or len(address["state"]) != 2:
        raise ValueError("Informe um CEP e uma UF válidos.")

    connection = _connect(db_path)
    try:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                INSERT OR IGNORE INTO profiles (email) VALUES (?)
                """,
                (normalized_email,),
            )
            existing = None
            if deduplicate:
                existing = connection.execute(
                    """
                    SELECT id, title, street, number, complement, neighborhood,
                           city, state, cep, is_main
                    FROM addresses
                    WHERE owner_email = ? AND street = ? COLLATE NOCASE
                      AND number = ? AND complement = ? COLLATE NOCASE
                      AND city = ? COLLATE NOCASE AND state = ? AND cep = ?
                    """,
                    (
                        normalized_email,
                        address["street"],
                        address["number"],
                        address["complement"],
                        address["city"],
                        address["state"],
                        address["cep"],
                    ),
                ).fetchone()
            if existing is not None:
                return {
                    "id": existing["id"],
                    **{key: existing[key] for key in address},
                    "is_main": bool(existing["is_main"]),
                }

            is_main = connection.execute(
                "SELECT 1 FROM addresses WHERE owner_email = ? LIMIT 1",
                (normalized_email,),
            ).fetchone() is None
            address_id = secrets.token_urlsafe(18)
            connection.execute(
                """
                INSERT INTO addresses (
                    id, owner_email, title, street, number, complement,
                    neighborhood, city, state, cep, is_main
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    address_id,
                    normalized_email,
                    address["title"],
                    address["street"],
                    address["number"],
                    address["complement"],
                    address["neighborhood"],
                    address["city"],
                    address["state"],
                    address["cep"],
                    int(is_main),
                ),
            )
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível salvar o endereço.") from exc
    finally:
        connection.close()

    return {"id": address_id, **address, "is_main": is_main}


def set_primary_address(
    email: str,
    address_id: str,
    *,
    db_path: Path | None = None,
) -> bool:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        return False

    connection = _connect(db_path)
    try:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            exists = connection.execute(
                "SELECT 1 FROM addresses WHERE owner_email = ? AND id = ?",
                (normalized_email, address_id),
            ).fetchone()
            if exists is None:
                return False
            connection.execute(
                "UPDATE addresses SET is_main = 0 WHERE owner_email = ?",
                (normalized_email,),
            )
            connection.execute(
                """
                UPDATE addresses SET is_main = 1
                WHERE owner_email = ? AND id = ?
                """,
                (normalized_email, address_id),
            )
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível atualizar o endereço principal.") from exc
    finally:
        connection.close()
    return True


def delete_address(
    email: str,
    address_id: str,
    *,
    db_path: Path | None = None,
) -> list[SavedAddress]:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        return []

    connection = _connect(db_path)
    try:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            deleted = connection.execute(
                "DELETE FROM addresses WHERE owner_email = ? AND id = ?",
                (normalized_email, address_id),
            ).rowcount
            if deleted:
                connection.execute(
                    """
                    UPDATE addresses SET is_main = 1
                    WHERE owner_email = ? AND id = (
                        SELECT id FROM addresses
                        WHERE owner_email = ?
                        ORDER BY created_at, id LIMIT 1
                    )
                    AND NOT EXISTS (
                        SELECT 1 FROM addresses
                        WHERE owner_email = ? AND is_main = 1
                    )
                    """,
                    (normalized_email, normalized_email, normalized_email),
                )
    except sqlite3.Error as exc:
        raise AuthStorageError("Não foi possível remover o endereço.") from exc
    finally:
        connection.close()
    return load_addresses(normalized_email, db_path=db_path)


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
