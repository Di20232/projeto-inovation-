## Purpose

Apresentar a NightFall como uma loja online de hardware com uma página inicial pública e reconhecível, deixando claro que o catálogo ainda não possui produtos disponíveis.

## ADDED Requirements

### Requirement: Identidade visual da NightFall
A página inicial SHALL exibir o nome NightFall e usar uma identidade visual predominantemente preta e roxa, com contraste suficiente para manter os textos e controles legíveis.

#### Scenario: Visitante abre a página inicial
- **WHEN** um visitante acessa a página inicial
- **THEN** o nome NightFall é visível em uma interface de tema escuro com roxo como cor de destaque e conteúdo legível

### Requirement: Catálogo inicialmente vazio
A página inicial SHALL informar que o catálogo está sendo preparado quando não houver produtos cadastrados e SHALL NOT apresentar produtos fictícios, preços, cards de produto, filtros ou ações de compra.

#### Scenario: Loja ainda não possui produtos
- **WHEN** não há produtos cadastrados para exibição
- **THEN** a página apresenta uma mensagem clara de catálogo em preparação e não sugere que existam produtos disponíveis

### Requirement: Acesso público e layout adaptável
A página inicial SHALL estar disponível sem autenticação e seu conteúdo SHALL permanecer legível em telas estreitas e amplas, sem rolagem horizontal da página.

#### Scenario: Visitante acessa sem autenticação
- **WHEN** um visitante abre a página inicial sem uma conta
- **THEN** o nome da loja e a mensagem de catálogo em preparação são exibidos sem exigir login

#### Scenario: Visitante usa uma tela estreita
- **WHEN** a página é visualizada em uma tela estreita
- **THEN** o nome da loja e a mensagem de estado vazio continuam legíveis sem rolagem horizontal
