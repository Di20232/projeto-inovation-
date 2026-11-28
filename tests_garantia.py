"""Testes da garantia: cadastro no catálogo e cálculo para o cliente."""

import json
import sys
import tempfile
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from python import python as app_module  # noqa: E402
from warranty import add_months, load_warranties_for_email, parse_warranty_months  # noqa: E402

PRODUCT = {
    "name": "Mouse Teste",
    "image_url": "https://exemplo.com/img.jpg",
    "price": 100.0,
    "description": "Produto de teste.",
    "category": "Periféricos",
}


def _build(**extra):
    return app_module.build_product(
        name="Mouse Teste",
        price_text="100",
        category="Periféricos",
        brand="",
        description="Produto de teste.",
        image_url="https://exemplo.com/img.jpg",
        **extra,
    )


def _warranties(orders, catalog=None, email="cliente@example.com", today=date(2026, 11, 27)):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "orders.json"
        path.write_text(json.dumps(orders), encoding="utf-8")
        return load_warranties_for_email(email, catalog or {}, path=path, today=today)


def _order(item, date_text="27/11/2026", email="cliente@example.com"):
    return {"id": "#NF-1", "date": date_text, "user_email": email, "items": [item]}


@pytest.mark.parametrize("text,months", [("", 0), ("  ", 0), ("0", 0), (" 12 ", 12), ("120", 120)])
def test_meses_validos(text, months):
    assert parse_warranty_months(text) == months


@pytest.mark.parametrize("text", ["-1", "121", "1,5", "doze", "²"])
def test_meses_invalidos(text):
    with pytest.raises(ValueError, match="Garantia inválida"):
        parse_warranty_months(text)


def test_soma_de_meses_respeita_fim_do_mes():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)
    assert add_months(date(2026, 11, 27), 12) == date(2027, 11, 27)
    assert add_months(date(2026, 12, 1), 1) == date(2027, 1, 1)


def test_produto_guarda_a_garantia_ao_salvar_e_recarregar():
    product = _build(warranty_text="12")
    assert product["warranty_months"] == 12
    saved = app_module._product_to_json(product)
    assert app_module.parse_catalog_data([saved])[0]["warranty_months"] == 12


def test_catalogo_antigo_sem_garantia_continua_valido():
    assert app_module.parse_catalog_data([PRODUCT])[0]["warranty_months"] == 0


@pytest.mark.parametrize("value", [-1, 121, "12", 1.5, True])
def test_catalogo_recusa_garantia_invalida(value):
    with pytest.raises(ValueError, match="Garantia"):
        app_module.parse_catalog_data([{**PRODUCT, "warranty_months": value}])


def test_compra_com_garantia_aparece_ativa():
    [item] = _warranties([_order({"name": "Mouse Teste", "warranty_months": 12})])
    assert item["expiry_date"] == "27/11/2027"
    assert item["status"] == "Ativa" and item["active"]


def test_vale_no_ultimo_dia_e_expira_no_seguinte():
    orders = [_order({"name": "Mouse Teste", "warranty_months": 1}, "27/10/2026")]
    assert _warranties(orders)[0]["status"] == "Ativa"
    assert _warranties(orders, today=date(2026, 11, 28))[0]["status"] == "Expirada"


def test_pedido_antigo_usa_o_prazo_do_catalogo():
    [item] = _warranties([_order({"name": "Mouse Teste"})], {"Mouse Teste": 6})
    assert item["months_display"] == "6 meses"


def test_prazo_gravado_na_compra_vale_mais_que_o_catalogo():
    orders = [_order({"name": "Mouse Teste", "warranty_months": 0})]
    assert _warranties(orders, {"Mouse Teste": 6}) == []


def test_cliente_nao_ve_garantia_de_outro():
    orders = [_order({"name": "Mouse Teste", "warranty_months": 12}, email="outra@example.com")]
    assert _warranties(orders) == []
    assert _warranties(orders, email="") == []
