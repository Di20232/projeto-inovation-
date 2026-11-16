# Proposal: Filtros Avançados Laterais (Preço, Marcas, Categorias)

## Contexto
O usuário solicitou adicionar ao lado dos produtos um painel de filtros avançados contendo:
- Filtro de faixa de preço (mínimo e máximo).
- Filtro por categorias.
- Filtro por marcas/especificações.

## Objetivo
1. Criar variáveis de estado em `CatalogState` para `min_price`, `max_price` e `selected_brands` (ou marcas).
2. Implementar uma barra/painel lateral de filtros à esquerda do catálogo de produtos.
3. Atualizar a propriedade computada `filtered_products` para filtrar cumulativamente por categoria, termo de pesquisa e faixa de preço.

## Escopo
- Criar change no OpenSpec (`2026-10-22-filtros-avancados-lateral`).
- Adicionar variáveis e eventos no `CatalogState` em `python/python.py`.
- Desenhar a barra lateral de filtros na interface.
- Consultar o conselho (Claude Council) para validar a arquitetura dos filtros reativos em Reflex.
