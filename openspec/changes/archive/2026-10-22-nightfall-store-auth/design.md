# Design: NightFall Storefront & Auth

## Arquitetura
- **Frontend**: Reflex (`python/python.py`), utilizando componentes reativos e páginas `/`, `/login` e `/cadastro`.
- **Catálogo**: Carregado de `python/catalog.json` com validação de esquema, preços formatados e categorias (Computadores, Componentes, Periféricos, Acessórios).
- **Autenticação**: Endpoint de signup e login integrado ao Xano.
