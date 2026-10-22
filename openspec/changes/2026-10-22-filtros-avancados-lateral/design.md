# Design: Filtros Laterais Avançados em Reflex

## Estado (`CatalogState`)
- `min_price: str = ""`
- `max_price: str = ""`
- `selected_brand: str = "Todas"`
- Métodos de evento para atualizar esses valores.

## Lógica de Filtragem (`filtered_products`)
- Filtra por categoria ativa (se diferente de "Todos").
- Filtra por termo de busca (`search_query`).
- Filtra por preço mínimo (`price >= float(min_price)`) se informado.
- Filtra por preço máximo (`price <= float(max_price)`) se informado.
- Filtra por marca (extraída das especificações do produto, ex: "Marca").

## Layout (`product_catalog`)
- Uso de `rx.flex` (direção `row`):
  - Coluna esquerda: Painel fixo de filtros (`width="280px"`):
    - Inputs para Preço Mínimo e Máximo.
    - Seção de Categorias.
    - Seção de Limpar Filtros.
  - Coluna direita (`flex="1"`):
    - Barra de pesquisa no topo.
    - Grid de produtos filtrados.
