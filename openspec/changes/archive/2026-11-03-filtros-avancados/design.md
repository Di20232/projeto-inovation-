# Design: Filtros Avançados de Preço e Marca

## Arquitetura e Componentes
- **Estado (`CatalogState`)**:
  - `min_price: str` e `max_price: str` para o intervalo de preço.
  - `selected_brand: str` para a marca selecionada (padrão `"Todas"`).
  - `brands: list[str]` computed var que extrai marcas únicas das especificações dos produtos.
  - `clear_filters` event handler para resetar filtros.
- **UI (`advanced_filters_panel`)**:
  - Bloco estilizado em gradiente escuro com inputs de preço mínimo e máximo.
  - Botões em grade/pills para cada marca disponível.
  - Botão "Limpar Filtros" para resetar rapidamente.
