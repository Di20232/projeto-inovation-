## ADDED Requirements

### Requirement: Botão visual do carrinho no cabeçalho
A página inicial SHALL exibir um botão com ícone de carrinho de compras ao lado do controle “Categorias”. O botão SHALL ter um rótulo acessível para leitores de tela e aparência consistente com os demais controles do cabeçalho. O botão SHALL ser apenas visual e SHALL NOT navegar, abrir conteúdo, alterar estado, exibir quantidade de itens ou executar ações de carrinho.

#### Scenario: Visitante vê o ícone do carrinho
- **WHEN** o visitante acessa a página inicial
- **THEN** um botão com ícone de carrinho é exibido ao lado do controle “Categorias”

#### Scenario: Tecnologia assistiva identifica o botão
- **WHEN** o botão do carrinho recebe foco ou é anunciado por um leitor de tela
- **THEN** ele possui um nome acessível que identifica o carrinho de compras

#### Scenario: Visitante ativa o botão visual
- **WHEN** o visitante clica ou ativa pelo teclado o botão do carrinho
- **THEN** nenhuma navegação, alteração de estado ou ação de compra é realizada

#### Scenario: Cabeçalho em tela estreita
- **WHEN** a página inicial é exibida em uma tela estreita
- **THEN** o botão do carrinho permanece visível junto ao controle “Categorias” sem causar rolagem horizontal
