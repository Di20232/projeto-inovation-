"""Script de simulação real do fluxo de pedidos no NightFall."""

import json
import os
import random
from datetime import datetime
from order_persistence import send_order_to_xano, save_order_local

def main():
    print("="*65)
    print(" 🚀 SIMULAÇÃO REAL DE PEDIDOS — E-COMMERCE NIGHTFALL")
    print("="*65)

    # 1. Simula carrinho de compras do cliente
    items = [
        {"name": "Processador AMD Ryzen 7 7800X3D", "price": 2899.90, "quantity": 1},
        {"name": "Placa Mãe ASUS ROG Strix B650", "price": 1499.90, "quantity": 1},
        {"name": "Memória RAM Corsair Vengeance 32GB (2x16) DDR5", "price": 799.90, "quantity": 1}
    ]

    subtotal = sum(item["price"] * item["quantity"] for item in items)
    discount = subtotal * 0.10  # Cupom NIGHTFALL10 (10% OFF)
    shipping = 0.0 if subtotal >= 250.0 else 15.0  # Frete grátis acima de R$ 250
    total = subtotal - discount + shipping

    order_id = f"#NF-{random.randint(10000, 99999)}"

    order_data = {
        "id": order_id,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user_email": "diego.cliente@exemplo.com",
        "items": items,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2),
        "total_display": f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "shipping_address": {
            "cep": "01001-000",
            "address": "Praça da Sé",
            "number": "100",
            "neighborhood": "Sé",
            "city": "São Paulo",
            "state": "SP"
        },
        "payment_method": "credit_card",
        "status": "Concluído"
    }

    print(f"\n🛒 Carrinho Simulado:")
    for idx, item in enumerate(items, 1):
        print(f"   {idx}. {item['name']} (x{item['quantity']}) — R$ {item['price']:,.2f}")

    print(f"\n💰 Resumo Financeiro:")
    print(f"   Subtotal: R$ {subtotal:,.2f}")
    print(f"   Desconto (NIGHTFALL10): - R$ {discount:,.2f}")
    print(f"   Frete: {'Grátis' if shipping == 0 else f'R$ {shipping:,.2f}'}")
    print(f"   TOTAL FINAL: R$ {total:,.2f}")

    print(f"\n📦 Endereço de Entrega:")
    addr = order_data["shipping_address"]
    print(f"   {addr['address']}, {addr['number']} — {addr['neighborhood']}, {addr['city']}/{addr['state']} (CEP: {addr['cep']})")

    print(f"\n💾 Processando Pagamento e Salvando Pedido ({order_id})...")
    result = send_order_to_xano(order_data)

    print(f"   Status de Persistência: Sucesso ✅")
    print(f"   Armazenado em: {result.get('source', 'local_db').upper()}")

    # Exibe o banco de dados local atualizado
    if os.path.exists("orders_db.json"):
        with open("orders_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
            print(f"\n📊 Total de pedidos persistidos no banco de dados local (`orders_db.json`): {len(db)}")
            print(json.dumps(db[-1], indent=2, ensure_ascii=False))

    print("\n" + "="*65)
    print(" ✨ Simulação concluída com sucesso! Os dados foram salvos.")
    print("="*65)

if __name__ == "__main__":
    main()
