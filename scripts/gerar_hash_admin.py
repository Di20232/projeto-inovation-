"""Gera a linha ADMIN_PASSWORD_HASH para o .env sem mostrar a senha na tela.

Uso (na raiz do projeto, com o venv ativo):
    python scripts/gerar_hash_admin.py
"""

import sys
from getpass import getpass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from admin_auth import hash_admin_password  # noqa: E402


def main() -> None:
    senha = getpass("Nova senha do admin: ")
    if len(senha) < 8:
        raise SystemExit("Use pelo menos 8 caracteres.")
    if getpass("Repita a senha: ") != senha:
        raise SystemExit("As senhas não conferem.")
    print("\nCole no .env (junto com ADMIN_EMAIL=...):")
    print(f"ADMIN_PASSWORD_HASH={hash_admin_password(senha)}")


if __name__ == "__main__":
    main()
