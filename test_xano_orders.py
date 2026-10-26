import httpx

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth"
ORDERS_URL = f"{BASE_URL}/orders"

def test_xano_orders():
    print("Testando envio de pedidos (orders) ao vivo no Xano...")

    order_payload = {
        "user_email": "teste.user@exemplo.com",
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

    try:
        response = httpx.post(ORDERS_URL, json=order_payload, timeout=10.0)
        print(f"Status Code (Orders): {response.status_code}")
        print(f"Resposta (Orders): {response.text}")
        if response.status_code in (200, 201):
            print("Sucesso! Pedido registrado no Xano.")
        else:
            print("Nota: Endpoint de orders pode não estar criado no Xano ainda (requer criação da tabela orders no painel Xano).")
    except Exception as e:
        print(f"Erro ao enviar pedido para o Xano: {e}")

if __name__ == "__main__":
    test_xano_orders()
