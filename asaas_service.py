import os
import httpx

ASAAS_SANDBOX_URL = "https://sandbox.asaas.com/api/v3"
ASAAS_PROD_URL = "https://api.asaas.com/v3"

def get_asaas_base_url() -> str:
    env = os.getenv("ASAAS_ENVIRONMENT", "sandbox").strip().lower()
    return ASAAS_PROD_URL if env == "production" else ASAAS_SANDBOX_URL

def get_asaas_headers() -> dict:
    api_key = os.getenv("ASAAS_API_KEY", "").strip()
    return {
        "access_token": api_key,
        "Content-Type": "application/json",
        "User-Agent": "NightFall-Store/1.0"
    }

def get_or_create_customer(name: str, email: str, cpf_cnpj: str, phone: str = "") -> str:
    """Retorna o ID do cliente no Asaas, criando-o se não existir."""
    base_url = get_asaas_base_url()
    headers = get_asaas_headers()

    # Busca cliente por email ou cpfCnpj
    try:
        with httpx.Client(timeout=15.0) as client:
            res = client.get(f"{base_url}/customers", params={"email": email}, headers=headers)
            if res.status_code == 200:
                data = res.json()
                customers = data.get("data", [])
                if customers:
                    return customers[0]["id"]

            # Se não encontrou, cria
            payload = {
                "name": name,
                "email": email,
                "cpfCnpj": "".join(filter(str.isdigit, cpf_cnpj)),
                "phone": phone
            }
            res_create = client.post(f"{base_url}/customers", json=payload, headers=headers)
            if res_create.status_code in (200, 201):
                return res_create.json()["id"]
    except Exception as e:
        print(f"Erro ao gerenciar cliente Asaas: {e}")
    return ""

def create_payment(customer_id: str, billing_type: str, value: float, description: str, credit_card: dict | None = None) -> dict:
    """Cria uma cobrança no Asaas (PIX, CREDIT_CARD, BOLETO)."""
    base_url = get_asaas_base_url()
    headers = get_asaas_headers()

    from datetime import datetime, timedelta
    due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    payload = {
        "customer": customer_id,
        "billingType": billing_type,
        "value": value,
        "dueDate": due_date,
        "description": description,
    }

    if billing_type == "CREDIT_CARD" and credit_card:
        payload["creditCard"] = credit_card
        payload["creditCardHolderInfo"] = credit_card.get("holderInfo", {})

    try:
        with httpx.Client(timeout=20.0) as client:
            res = client.post(f"{base_url}/payments", json=payload, headers=headers)
            if res.status_code in (200, 201):
                payment_data = res.json()
                payment_id = payment_data.get("id")

                result = {
                    "success": True,
                    "payment_id": payment_id,
                    "status": payment_data.get("status"),
                    "invoice_url": payment_data.get("invoiceUrl"),
                }

                # Se for Pix, busca o QR Code
                if billing_type == "PIX" and payment_id:
                    res_pix = client.get(f"{base_url}/payments/{payment_id}/pixQrCode", headers=headers)
                    if res_pix.status_code == 200:
                        pix_data = res_pix.json()
                        result["pix_qr_code_url"] = pix_data.get("encodedImage")
                        result["pix_copy_paste"] = pix_data.get("payload")

                return result
            else:
                return {
                    "success": False,
                    "error": res.text
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
