"""Script para testar e lidar com pedidos no NightFall, com fallback para persistência local caso o endpoint Xano não esteja ativo."""

import httpx
import json
from pathlib import Path

ORDERS_FILE = Path(__file__).with_name("orders_db.json")
DEFAULT_XANO_ORDERS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/orders"

def save_order_local(order_data: dict) -> dict:
    """Salva o pedido em um arquivo JSON local para persistência garantida."""
    orders = []
    if ORDERS_FILE.exists():
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)
        except Exception:
            orders = []

    orders.append(order_data)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    return {"success": True, "source": "local_db", "order": order_data}

def send_order_to_xano(order_data: dict) -> dict:
    """Tenta enviar o pedido para o Xano. Se falhar, salva localmente."""
    try:
        response = httpx.post(DEFAULT_XANO_ORDERS_URL, json=order_data, timeout=5.0)
        if response.status_code in (200, 201):
            return {"success": True, "source": "xano", "data": response.json()}
    except Exception:
        pass

    # Fallback robusto para persistência local
    return save_order_local(order_data)

if __name__ == "__main__":
    test_order = {
        "user_email": "teste.user@exemplo.com",
        "total": 2609.91,
        "status": "pending"
    }
    print("Testando salvamento de pedido:", send_order_to_xano(test_order))
