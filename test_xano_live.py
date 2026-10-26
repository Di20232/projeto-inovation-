import httpx
import time

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth"
SIGNUP_URL = f"{BASE_URL}/signup"

def test_xano_signup():
    print("Testando criação de conta (signup) ao vivo no Xano...")

    unique_email = f"teste.user.{int(time.time())}@exemplo.com"
    password = "Password123!"

    signup_payload = {
        "name": "Diego Teste",
        "cpf": "12345678909",
        "birth_date": "1995-05-15",
        "email": unique_email,
        "password": password
    }
    try:
        response = httpx.post(SIGNUP_URL, json=signup_payload, timeout=10.0)
        print(f"Status Code (Signup): {response.status_code}")
        print(f"Resposta (Signup): {response.text}")
        if response.status_code == 200:
            print("Sucesso! Conta criada e registrada no Xano.")
    except Exception as e:
        print(f"Erro no signup: {e}")

if __name__ == "__main__":
    test_xano_signup()
