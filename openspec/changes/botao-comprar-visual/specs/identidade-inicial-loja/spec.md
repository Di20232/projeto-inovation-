## ADDED Requirements

### Requirement: Botão visual “Comprar +” nos produtos do catálogo
A página inicial SHALL exibir um botão verde com o texto “Comprar +” em cada card de produto do catálogo. O botão SHALL ter um nome acessível que identifique a ação visual e o produto correspondente. O botão SHALL ser apenas visual: ativá-lo SHALL NOT adicionar o produto ao carrinho, alterar estado, navegar, abrir os detalhes do produto ou executar outra ação.

#### Scenario: Visitante vê o botão em cada produto
- **WHEN** o catálogo exibe um ou mais produtos
- **THEN** cada card de produto exibe um botão verde “Comprar +”

#### Scenario: Tecnologia assistiva identifica o botão
- **WHEN** o botão “Comprar +” recebe foco ou é anunciado por um leitor de tela
- **THEN** seu nome acessível identifica “Comprar” e o produto associado

#### Scenario: Visitante ativa o botão visual
- **WHEN** o visitante clica ou ativa pelo teclado o botão “Comprar +”
- **THEN** nenhum produto é adicionado ao carrinho e nenhuma navegação, abertura de detalhes ou alteração de estado acontece

#### Scenario: Visitante usa o botão em tela estreita
- **WHEN** os cards de produtos são exibidos em uma tela estreita
- **THEN** o botão permanece visível, legível e utilizável sem causar rolagem horizontal
