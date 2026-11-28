"""Testes da lista de pedidos do painel administrativo."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from order_persistence import load_all_orders  # noqa: E402


def _load(content: str) -> list[dict]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "orders.json"
        path.write_text(content, encoding="utf-8")
        return load_all_orders(path)


def test_lista_pedidos_de_todos_os_clientes_do_mais_recente_ao_mais_antigo():
    orders = [
        {"id": "#1", "user_email": "um@example.com", "total_display": "R$ 10,00"},
        {"id": "#2", "user_email": "dois@example.com", "total_display": "R$ 20,00"},
    ]
    result = _load(json.dumps(orders))
    assert [o["id"] for o in result] == ["#2", "#1"]
    assert [o["customer"] for o in result] == ["dois@example.com", "um@example.com"]


def test_mostra_itens_e_aceita_pedido_antigo_incompleto():
    orders = [
        {
            "id": "#antigo",
            "total": 2609.91,
            "items": [{"name": "Mouse", "quantity": 2}, {"name": "SSD"}],
        }
    ]
    [order] = _load(json.dumps(orders))
    assert order["customer"] == "Cliente não identificado"
    assert order["items_summary"] == "2x Mouse, 1x SSD"
    assert order["total_display"] == "R$ 2.609,91"


def test_arquivo_ausente_ou_invalido_devolve_lista_vazia():
    assert load_all_orders(Path("nao-existe.json")) == []
    assert _load("isto nao e json") == []
    assert _load('{"id": "#1"}') == []
