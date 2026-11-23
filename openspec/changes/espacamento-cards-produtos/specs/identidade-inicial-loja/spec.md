## ADDED Requirements

### Requirement: Espaçamento dos cards de produto
O catálogo SHALL apresentar os produtos em duas colunas com uma distância visual pequena, porém clara, entre cards adjacentes. Os cards SHALL continuar ocupando toda a largura disponível em cada coluna e SHALL NOT alterar a quantidade de itens por linha.

#### Scenario: Visitante vê o catálogo completo
- **WHEN** o visitante abre o catálogo em uma largura compatível com o layout atual
- **THEN** os produtos são exibidos em duas colunas e existe espaçamento visível entre cada card horizontal e verticalmente adjacente

#### Scenario: Visitante compara cards adjacentes
- **WHEN** dois produtos são exibidos lado a lado
- **THEN** os limites dos dois cards permanecem claramente separados sem que o espaçamento faça a grade ocupar menos do que a largura do conteúdo
