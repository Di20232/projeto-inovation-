# Proposta: Carrinho de Compras Interativo na Vitrine NightFall

## Contexto
A vitrine virtual NightFall exibia um ícone de carrinho de compras estático e puramente visual. Os usuários não conseguiam adicionar produtos, gerenciar quantidades ou visualizar o subtotal da compra.

## Objetivo
Implementar o fluxo completo de carrinho de compras na aplicação Reflex (`python/python.py`), permitindo adicionar produtos ao carrinho, ajustar quantidades, remover itens, visualizar a contagem de itens em badge no cabeçalho e calcular o subtotal com formatação monetária.

## Escopo
- Estado reativo de carrinho em `CatalogState` (`cart_items`, `cart_open`).
- Ações de adicionar, remover, atualizar quantidade e esvaziar carrinho.
- Drawer lateral deslizante (`cart_drawer`) com listagem de itens e subtotal.
- Badge interativo no ícone do carrinho no cabeçalho.
- Botão "Adicionar ao carrinho" na modal de detalhes do produto.
