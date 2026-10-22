## Purpose
Remover textos introdutórios da home e tornar a barra de pesquisa expansível e proeminente no topo.

## ADDED Requirements

### Requirement: Remoção de textos de introdução
O sistema SHALL não exibir blocos de texto promocional/introdutório genérico na página inicial.

#### Scenario: Visualização da home limpa
- **WHEN** o usuário acessa a página inicial (`/`)
- **THEN** o catálogo e as categorias aparecem diretamente sem os textos de introdução.

### Requirement: Barra de pesquisa no topo com expansão no foco
A barra de pesquisa SHALL ficar no topo da vitrine e expandir suavemente (com animação/sombra) ao receber foco.

#### Scenario: Foco na barra de pesquisa
- **WHEN** o usuário clica ou foca na barra de pesquisa
- **THEN** ela expande com destaque visual refinado.
