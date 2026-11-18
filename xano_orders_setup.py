"""Script para configurar o endpoint de pedidos (orders) no Xano e testar persistência."""

import httpx

XANO_BASE = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth"

def create_order(payload: dict) -> dict:
    """Cria um pedido no Xano."""
    try:
        response = httpx.post(f"{XANO_BASE}/orders", json=payload, timeout=10.0)
        return {
            "status_code": response.status_code,
            "body": response.json(),
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    order_payload = {
        "user_email": "teste.user.1794955463@exemplo.com",
        "items": [
            {"name": "Processador AMD Ryzen 7 7800X3D", "price": 2899.90, "quantity": 1}
        ],
        "subtotal": 2899.90,
        "discount": 289.99,
        "shipping": 0.0,
        "total": 2609.91,
        "shipping_address": {
            "cep": "01001-000",
            "address": "Praça da Sé",
            "number": "100",
            "neighborhood": "Sé",
            "city": "São Paulo",
            "state": "SP"
        },
        "payment_method": "credit_card",
        "status": "pending"
    }
    result = create_order(order_payload)
    print(result)
