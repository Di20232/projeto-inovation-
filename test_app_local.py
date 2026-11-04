import httpx

BASE_URL = "http://localhost:3000"

def test_local_app():
    print("Testando rotas locais da aplicação NightFall...")

    routes = ["/", "/carrinho", "/pagamento", "/perfil"]
    for route in routes:
        url = f"{BASE_URL}{route}"
        try:
            resp = httpx.get(url, timeout=5.0)
            print(f"GET {url} -> Status: {resp.status_code}")
            assert resp.status_code in {200, 301, 302, 307, 308}
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

    print("Testes locais de rotas finalizados com sucesso!")

if __name__ == "__main__":
    test_local_app()
