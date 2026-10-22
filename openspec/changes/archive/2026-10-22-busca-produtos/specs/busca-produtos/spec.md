## Purpose

Permitir que visitantes encontrem produtos do catálogo NightFall por texto, usando a busca junto com o filtro de categoria.

## ADDED Requirements

### Requirement: Pesquisa textual de produtos
A página inicial SHALL permitir pesquisar produtos por nome, descrição, categoria, rótulos e valores de especificações técnicas, sem distinção entre letras maiúsculas e minúsculas. A busca SHALL ser aplicada em conjunto com a categoria selecionada e SHALL atualizar os resultados conforme o texto informado.

#### Scenario: Visitante pesquisa por nome ou especificação
- **WHEN** o visitante informa um termo que aparece no nome, descrição, categoria ou especificações de um produto
- **THEN** o catálogo exibe somente produtos que correspondem ao termo e à categoria atualmente selecionada

#### Scenario: Pesquisa não encontra produtos
- **WHEN** o visitante informa um termo sem correspondência no catálogo ou na categoria selecionada
- **THEN** a página informa que nenhum produto foi encontrado para a pesquisa e não exibe cards

#### Scenario: Visitante limpa a pesquisa
- **WHEN** o visitante remove o texto do campo de pesquisa
- **THEN** o catálogo volta a exibir todos os produtos da categoria selecionada
