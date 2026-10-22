# Tasks: Catálogo via Xano

## 1. Especificação
- [x] 1.1 Criar change OpenSpec para integração de produtos com Xano
- [x] 1.2 Documentar requisitos em `specs/xano-produtos/spec.md`

## 2. Implementação
- [x] 2.1 Atualizar `.env.example` com `XANO_PRODUCTS_URL`
- [x] 2.2 Atualizar `load_catalog()` em `python/python.py` para consultar Xano com fallback local
- [ ] 2.3 Validar carregamento com o endpoint ativo do Xano
