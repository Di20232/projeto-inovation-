# Design: Carrinho de Compras

## Arquitetura e Decisões
- **Estado**: Adicionados `cart_items` e `cart_open` a `CatalogState` em `python/python.py`.
- **Componentes**:
  - `cart_drawer`: Modal deslizante à direita para exibição dos itens e ações de checkout.
  - `cart_item_row`: Linha individual de produto no carrinho com controles de quantidade (`+` / `-`) e remoção.
  - Badge reativo no cabeçalho indicando a quantidade de itens.
- **Formatação de Moeda**: Utilização de `Decimal` e formatação PT-BR (`R$ X,XX`).
