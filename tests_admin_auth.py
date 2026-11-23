"""Testes da autenticação no servidor (admin_auth.py). Rodam sem rede: o Xano é simulado."""

import os
import sys

import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import admin_auth  # noqa: E402
from admin_auth import (  # noqa: E402
    XanoUnavailable,
    check_env_admin,
    hash_admin_password,
    verify_admin_password,
    xano_login,
)

FAST = 1_000  # iterações baixas só para o teste ficar rápido


def _with_env(**values):
    old = {k: os.environ.get(k) for k in values}
    for k, v in values.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    return old


def _restore(old):
    _with_env(**old)


def test_hash_e_verificacao():
    h = hash_admin_password("segredo-forte", iterations=FAST)
    assert h.startswith("pbkdf2_sha256:") and "segredo-forte" not in h and "$" not in h
    assert verify_admin_password("segredo-forte", h)
    assert not verify_admin_password("errada", h)
    assert hash_admin_password("x", iterations=FAST) != hash_admin_password("x", iterations=FAST)  # salt aleatório


def test_hash_invalido_nao_quebra():
    for ruim in ("", "texto", "md5:1:aa:bb", "pbkdf2_sha256:abc:zz:yy"):
        assert not verify_admin_password("qualquer", ruim)


def test_admin_do_env():
    old = _with_env(ADMIN_EMAIL="Admin@Loja.com", ADMIN_PASSWORD_HASH=hash_admin_password("certa123", iterations=FAST))
    try:
        assert check_env_admin("admin@loja.com", "certa123")
        assert check_env_admin(" ADMIN@LOJA.COM ", "certa123")
        assert not check_env_admin("admin@loja.com", "errada")
        assert not check_env_admin("outro@loja.com", "certa123")
    finally:
        _restore(old)


def test_sem_env_ninguem_e_admin():
    old = _with_env(ADMIN_EMAIL=None, ADMIN_PASSWORD_HASH=None)
    try:
        assert not check_env_admin("admin@admin.com", "admin123")
    finally:
        _restore(old)


def test_reconhece_email_do_admin():
    old = _with_env(ADMIN_EMAIL="Admin@Loja.com")
    try:
        assert admin_auth.is_env_admin_email(" admin@loja.com ")
        assert not admin_auth.is_env_admin_email("outro@loja.com")
        _with_env(ADMIN_EMAIL=None)
        assert not admin_auth.is_env_admin_email("admin@loja.com")
        assert not admin_auth.is_env_admin_email("")
    finally:
        _restore(old)


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_xano_nao_configurado_devolve_none():
    old = _with_env(XANO_LOGIN_URL=None)
    try:
        assert xano_login("a@b.com", "x") is None
    finally:
        _restore(old)


def test_xano_admin_e_cliente():
    old = _with_env(XANO_LOGIN_URL="https://xano.test/api:nightfall-auth/login")
    try:
        def handler(request):
            body = request.read().decode()
            if '"admin@loja.com"' in body:
                return httpx.Response(200, json={"authToken": "tok-a", "user": {"is_admin": True}})
            return httpx.Response(200, json={"authToken": "tok-c", "user": {"is_admin": False}})

        r = xano_login("admin@loja.com", "x", client=_client(handler))
        assert r.ok and r.is_admin and r.token == "tok-a"
        r = xano_login("cliente@loja.com", "x", client=_client(handler))
        assert r.ok and not r.is_admin
    finally:
        _restore(old)


def test_xano_is_admin_precisa_ser_true_de_verdade():
    old = _with_env(XANO_LOGIN_URL="https://xano.test/login")
    try:
        for valor in ("true", 1, "yes", None):
            r = xano_login("a@b.com", "x", client=_client(
                lambda req, v=valor: httpx.Response(200, json={"authToken": "t", "user": {"is_admin": v}})))
            assert r.ok and not r.is_admin, valor
    finally:
        _restore(old)


def test_xano_credenciais_invalidas():
    old = _with_env(XANO_LOGIN_URL="https://xano.test/login")
    try:
        for status in (400, 401, 403):
            r = xano_login("a@b.com", "x", client=_client(lambda req, s=status: httpx.Response(s, json={})))
            assert r is not None and not r.ok and not r.is_admin
    finally:
        _restore(old)


def test_xano_indisponivel():
    old = _with_env(XANO_LOGIN_URL="https://xano.test/login")
    try:
        casos = [
            lambda req: httpx.Response(404, json={}),
            lambda req: httpx.Response(500, text="erro"),
            lambda req: httpx.Response(200, text="não é json"),
            lambda req: httpx.Response(200, json={"user": {"is_admin": True}}),  # sem token
        ]
        def rede(req):
            raise httpx.ConnectError("sem rede")
        casos.append(rede)
        for handler in casos:
            try:
                xano_login("a@b.com", "x", client=_client(handler))
                raise AssertionError("deveria lançar XanoUnavailable")
            except XanoUnavailable:
                pass
    finally:
        _restore(old)


if __name__ == "__main__":
    total = 0
    for nome, func in sorted(globals().items()):
        if nome.startswith("test_") and callable(func):
            func()
            total += 1
            print("OK", nome)
    print(f"{total} testes passaram")
    assert admin_auth.DEFAULT_ITERATIONS >= 600_000
