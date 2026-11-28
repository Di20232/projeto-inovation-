"""Testes do cupom e da gravação do perfil."""

import sys
import tempfile
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from auth_persistence import (  # noqa: E402
    authenticate_account,
    create_account,
    load_profile,
    save_profile,
)
from python import python as app_module  # noqa: E402

TODAY = date(2026, 11, 27)
CPF = "52998224725"


@pytest.mark.parametrize(
    "subtotal,expected",
    [(149.9, 14.99), (149.9 * 3, 44.97), (0, 0.0), (0.05, 0.01)],
)
def test_desconto_acompanha_o_subtotal(subtotal, expected):
    assert app_module.coupon_discount(subtotal, True) == expected


def test_sem_cupom_nao_ha_desconto():
    assert app_module.coupon_discount(449.7, False) == 0.0


def test_dados_validos_podem_ser_salvos():
    assert app_module.profile_problem("Pessoa", CPF, "01/01/1990", today=TODAY) == ""


@pytest.mark.parametrize(
    "name,cpf,birth,message",
    [
        (" ", CPF, "01/01/1990", "nome"),
        ("Pessoa", "11111111111", "01/01/1990", "CPF"),
        ("Pessoa", CPF, "31/02/2000", "Data"),
        ("Pessoa", CPF, "28/11/2026", "Data"),
        ("Pessoa", CPF, "", "Data"),
    ],
)
def test_dados_invalidos_sao_recusados(name, cpf, birth, message):
    assert message in app_module.profile_problem(name, cpf, birth, today=TODAY)


def test_perfil_salvo_permanece_e_a_senha_continua_valendo():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "users.sqlite3"
        create_account(
            name="Nome Antigo", email="cliente@example.com", cpf=CPF,
            birth_date="01/01/1990", password="senha-de-teste", db_path=db_path,
        )
        save_profile(
            "cliente@example.com", name="Nome Novo", cpf=CPF,
            birth_date="02/02/1992", db_path=db_path,
        )
        assert load_profile("cliente@example.com", db_path=db_path)["name"] == "Nome Novo"
        account = authenticate_account(
            "cliente@example.com", "senha-de-teste", db_path=db_path
        )
        assert account["name"] == "Nome Novo"
        assert account["birth_date"] == "02/02/1992"


def test_perfil_sem_conta_local_tambem_e_salvo():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "users.sqlite3"
        save_profile(
            "admin@example.com", name="Admin", cpf=CPF,
            birth_date="01/01/1990", db_path=db_path,
        )
        assert load_profile("admin@example.com", db_path=db_path)["name"] == "Admin"
