import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from auth_persistence import (
    AccountAlreadyExists,
    authenticate_account,
    create_account,
)


def test_cadastro_persiste_hash_e_exige_senha_correta():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "users.sqlite3"
        account = create_account(
            name="Pessoa Teste",
            email="Pessoa@Exemplo.com",
            cpf="12345678909",
            birth_date="01/01/1990",
            password="senha-correta-123",
            db_path=db_path,
        )

        assert account["email"] == "pessoa@exemplo.com"
        assert authenticate_account(" PESSOA@EXEMPLO.COM ", "senha-correta-123", db_path=db_path) == account
        assert authenticate_account("pessoa@exemplo.com", "senha-incorreta", db_path=db_path) is None

        connection = sqlite3.connect(db_path)
        try:
            password_hash = connection.execute(
                "SELECT password_hash FROM users WHERE email = ?",
                ("pessoa@exemplo.com",),
            ).fetchone()[0]
        finally:
            connection.close()
        assert password_hash.startswith("pbkdf2_sha256:")
        assert "senha-correta-123" not in password_hash


def test_cadastro_rejeita_email_duplicado_ignorando_maiusculas():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "users.sqlite3"
        create_account(
            name="Pessoa Teste",
            email="pessoa@exemplo.com",
            cpf="12345678909",
            birth_date="01/01/1990",
            password="senha-correta-123",
            db_path=db_path,
        )

        try:
            create_account(
                name="Outra Pessoa",
                email="PESSOA@EXEMPLO.COM",
                cpf="98765432100",
                birth_date="02/02/1990",
                password="outra-senha-segura",
                db_path=db_path,
            )
        except AccountAlreadyExists:
            pass
        else:
            raise AssertionError("o cadastro duplicado deveria ser recusado")


def test_login_de_conta_inexistente_e_email_invalido_sao_recusados():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "users.sqlite3"
        assert authenticate_account("inexistente@exemplo.com", "qualquer-senha", db_path=db_path) is None
        assert authenticate_account("email-invalido", "qualquer-senha", db_path=db_path) is None


def test_banco_local_aceita_caminho_configuravel():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "configured.sqlite3"
        with patch.dict(os.environ, {"NIGHTFALL_AUTH_DB": str(db_path)}):
            assert authenticate_account("inexistente@exemplo.com", "senha") is None
        assert db_path.exists()


if __name__ == "__main__":
    for test in (
        test_cadastro_persiste_hash_e_exige_senha_correta,
        test_cadastro_rejeita_email_duplicado_ignorando_maiusculas,
        test_login_de_conta_inexistente_e_email_invalido_sao_recusados,
        test_banco_local_aceita_caminho_configuravel,
    ):
        test()
        print("OK", test.__name__)
