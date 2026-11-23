"""Autenticação do NightFall no servidor: admin pelo .env e login pelo Xano.

Duas fontes de verdade, nenhuma no código-fonte:

1. Admin local (.env): ADMIN_EMAIL + ADMIN_PASSWORD_HASH (PBKDF2-SHA256).
   Gere o hash com:  python scripts/gerar_hash_admin.py
2. Xano (opcional): se XANO_LOGIN_URL estiver configurada, o login é feito no
   endpoint `login` do grupo nightfall-auth, que devolve `user.is_admin`.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass

import httpx

HASH_SCHEME = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 600_000


def hash_admin_password(password: str, *, iterations: int = DEFAULT_ITERATIONS, salt: str | None = None) -> str:
    """Devolve 'pbkdf2_sha256:<iterações>:<salt hex>:<hash hex>' (sem '$', para não brigar com o .env)."""
    if not password:
        raise ValueError("A senha não pode ser vazia.")
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), iterations)
    return f"{HASH_SCHEME}:{iterations}:{salt}:{digest.hex()}"


def verify_admin_password(password: str, encoded: str) -> bool:
    try:
        scheme, iterations, salt, expected = encoded.strip().split(":")
        if scheme != HASH_SCHEME:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), expected)


def check_env_admin(email: str, password: str) -> bool:
    """True só se ADMIN_EMAIL e ADMIN_PASSWORD_HASH existirem e baterem com o login."""
    admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    admin_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip()
    if not admin_email or not admin_hash:
        return False
    if not hmac.compare_digest((email or "").strip().lower(), admin_email):
        # Ainda roda o hash para não revelar, pelo tempo, se o e-mail é o do admin.
        verify_admin_password(password or "", admin_hash)
        return False
    return verify_admin_password(password or "", admin_hash)


class XanoUnavailable(Exception):
    """O Xano não respondeu de forma utilizável (rede, 404, 5xx, JSON inválido)."""


@dataclass
class XanoLoginResult:
    ok: bool
    is_admin: bool = False
    token: str = ""
    name: str = ""


def xano_login_url() -> str:
    return os.getenv("XANO_LOGIN_URL", "").strip()


def xano_login(email: str, password: str, *, client: httpx.Client | None = None) -> XanoLoginResult | None:
    """Faz o login no Xano. Devolve None se XANO_LOGIN_URL não estiver configurada.

    - 200 com authToken: ok=True e is_admin vindo de user.is_admin (o servidor decide).
    - 400/401/403: ok=False (credenciais inválidas).
    - Qualquer outra coisa: XanoUnavailable.
    """
    url = xano_login_url()
    if not url:
        return None
    own_client = client is None
    client = client or httpx.Client(timeout=8.0)
    try:
        response = client.post(url, json={"email": email, "password": password})
    except httpx.HTTPError as exc:
        raise XanoUnavailable(str(exc)) from exc
    finally:
        if own_client:
            client.close()

    if response.status_code in (400, 401, 403):
        return XanoLoginResult(ok=False)
    if response.status_code != 200:
        raise XanoUnavailable(f"HTTP {response.status_code}")
    try:
        data = response.json()
    except ValueError as exc:
        raise XanoUnavailable("JSON inválido") from exc
    if not isinstance(data, dict):
        raise XanoUnavailable("resposta não é um objeto JSON")
    token = data.get("authToken")
    if not isinstance(token, str) or not token:
        raise XanoUnavailable("resposta sem authToken")
    raw_user = data.get("user")
    user: dict = raw_user if isinstance(raw_user, dict) else {}
    return XanoLoginResult(
        ok=True,
        is_admin=user.get("is_admin") is True,
        token=token,
        name=str(user.get("name") or ""),
    )
