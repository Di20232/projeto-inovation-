## ADDED Requirements

### Requirement: Navegação lateral por categorias
A página inicial SHALL oferecer um controle acessível que abre um menu lateral com as categorias Computadores, Componentes, Periféricos e Acessórios. O menu SHALL poder ser fechado pelo próprio controle, pela tecla Escape ou pela ativação da área externa ao menu, sem causar rolagem horizontal da página.

#### Scenario: Visitante abre e fecha o menu
- **WHEN** o visitante ativa o controle de categorias
- **THEN** o menu lateral é exibido e pode ser fechado pelo controle, pela tecla Escape ou pela área externa ao menu

#### Scenario: Visitante navega pelo menu em tela estreita
- **WHEN** o menu é aberto em uma tela estreita
- **THEN** as categorias permanecem legíveis e utilizáveis sem rolagem horizontal da página

### Requirement: Categorias indisponíveis enquanto o catálogo está vazio
Enquanto não houver produtos disponíveis, cada categoria SHALL ser identificada com o estado “Em breve” e SHALL NOT permitir navegação para resultados inexistentes nem apresentar produtos fictícios.

#### Scenario: Visitante consulta uma categoria antes da disponibilização do catálogo
- **WHEN** o menu é exibido enquanto o catálogo não possui produtos
- **THEN** as quatro categorias mostram “Em breve” e não indicam resultados ou produtos disponíveis
