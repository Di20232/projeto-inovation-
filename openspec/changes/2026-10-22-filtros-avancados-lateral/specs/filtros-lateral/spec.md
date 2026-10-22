## Purpose
Adicionar painel lateral de filtros avançados (faixa de preço mínima/máxima e categorias) na vitrine de produtos.

## ADDED Requirements

### Requirement: Filtro de faixa de preço e categorias na lateral
O sistema SHALL exibir um painel lateral esquerdo com opções de filtragem por preço mínimo, preço máximo e categorias.

#### Scenario: Aplicação de filtro de preço
- **WHEN** o usuário define o preço mínimo e máximo no painel lateral
- **THEN** o catálogo exibe apenas os produtos cujos preços estão dentro da faixa especificada.
