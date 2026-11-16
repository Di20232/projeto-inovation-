# Design: Integração do Catálogo com Xano

## Arquitetura
- **Carregamento**: `load_catalog()` tentará consultar `XANO_PRODUCTS_URL` (configurável via `.env`). Se obtiver sucesso, processará e exibirá os itens do Xano. Caso contrário, usará `catalog.json`.
- **Formato**: Espera-se que o Xano retorne uma lista de produtos compatível com a estrutura de dicionários da aplicação (name, image_url, price, description, category, specifications).

## Verificação
- Testar comportamento com URL válida/inválida do Xano e verificar o fallback para `catalog.json`.
