import json
import httpx
from pathlib import Path

ENDPOINTS = [
    "https://x8ki-letl-twmt.n7.xano.io/api:produtoCRUD/produto",
    "https://x8ki-letl-twmt.n7.xano.io/api:produtocrud/produto",
    "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/produto",
]

def seed():
    catalog_path = Path("python/catalog.json")
    if not catalog_path.exists():
        print("catalog.json não encontrado.")
        return

    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    print(f"Carregados {len(data)} produtos do catálogo local. Cadastrando no Xano...")

    for i, item in enumerate(data, start=1):
        payload = {
            "produto": item.get("name"),
            "price": item.get("price"),
            "category": item.get("category"),
            "description": item.get("description"),
            "image_url": item.get("image_url"),
            "source_url": item.get("source_url")
        }

        success = False
        for url in ENDPOINTS:
            try:
                resp = httpx.post(url, json=payload, timeout=10.0)
                if resp.status_code == 200:
                    print(f"[{i}/{len(data)}] {payload['produto']} -> Sucesso em {url}")
                    success = True
                    break
                else:
                    print(f"[{i}/{len(data)}] {payload['produto']} -> {url} returned {resp.status_code}: {resp.text}")
            except Exception as e:
                print(f"Erro em {url}: {e}")

        if not success:
            print(f"Falha ao cadastrar: {payload['produto']}")

if __name__ == "__main__":
    seed()
