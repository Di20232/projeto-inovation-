## MODIFIED Requirements

### Requirement: Navegação lateral por categorias
A página inicial SHALL oferecer um controle acessível que abre um menu lateral com as categorias Computadores, Componentes, Periféricos e Acessórios. O menu SHALL poder ser fechado pelo próprio controle, pela tecla Escape ou pela ativação da área externa ao menu, sem causar rolagem horizontal da página. O menu SHALL apresentar uma hierarquia tipográfica legível e consistente, espaçamento suficiente entre o cabeçalho e as opções e alvos de interação confortáveis. A categoria ativa, incluindo “Todos os produtos” quando selecionado, SHALL ser visualmente distinguível das demais opções. A tipografia SHALL usar fontes locais do sistema com fallbacks legíveis, sem exigir carregamento externo.

#### Scenario: Visitante abre e fecha o menu
- **WHEN** o visitante ativa o controle de categorias
- **THEN** o menu lateral é exibido e pode ser fechado pelo controle, pela tecla Escape ou pela área externa ao menu

#### Scenario: Visitante navega pelo menu em tela estreita
- **WHEN** o menu é aberto em uma tela estreita
- **THEN** as categorias permanecem legíveis e utilizáveis sem rolagem horizontal da página

#### Scenario: Visitante identifica a categoria ativa
- **WHEN** uma categoria ou “Todos os produtos” está selecionado
- **THEN** a opção correspondente é visualmente distinguível das opções não selecionadas sem depender apenas de texto adicional

#### Scenario: Visitante lê as opções do menu
- **WHEN** o visitante abre o menu lateral
- **THEN** o cabeçalho e as opções usam hierarquia tipográfica consistente, espaçamento claro entre itens e fontes locais legíveis
