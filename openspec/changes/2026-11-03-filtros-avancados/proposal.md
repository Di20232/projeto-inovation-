# Proposal: Filtros Avançados de Preço e Marca no Catálogo

## Contexto
O usuário solicitou implementar os filtros avançados na vitrine de produtos da loja NightFall.

## Objetivo
1. Disponibilizar controles interativos para filtragem por faixa de preço (mínimo e máximo).
2. Disponibilizar seleção rápida de marcas extraídas dinamicamente das especificações dos produtos.
3. Permitir limpar todos os filtros aplicados com um único clique.

## Escopo
- Adicionar painel de filtros avançados no topo do catálogo em `python/python.py`.
- Integrar os controles com `min_price`, `max_price`, `selected_brand` e `clear_filters` em `CatalogState`.
- Compilar e testar a aplicação com `reflex compile --dry`.
