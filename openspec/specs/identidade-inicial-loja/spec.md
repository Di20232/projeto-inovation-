# identidade-inicial-loja Specification

## Purpose

Apresentar a NightFall como uma loja online de hardware com uma página inicial pública e reconhecível, deixando claro que o catálogo ainda não possui produtos disponíveis.

## Requirements

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

### Requirement: Categorias indisponíveis enquanto o catálogo está vazio
Enquanto não houver produtos disponíveis na respectiva categoria, ela SHALL ser identificada com o estado “Em breve” e SHALL NOT permitir navegação para resultados inexistentes nem apresentar produtos fictícios. Quando houver produtos reais cadastrados em uma categoria, essa categoria SHALL permitir a filtragem do catálogo por seus produtos. Os campos de imagem e página de origem de cada produto SHALL conter URLs HTTP ou HTTPS válidas.

#### Scenario: Visitante consulta uma categoria antes da disponibilização do catálogo
- **WHEN** o menu é exibido enquanto o catálogo não possui produtos
- **THEN** as quatro categorias mostram “Em breve” e não indicam resultados ou produtos disponíveis

#### Scenario: Visitante seleciona uma categoria disponível
- **WHEN** o menu é exibido e há produtos cadastrados em uma categoria
- **THEN** essa categoria pode ser selecionada para filtrar o catálogo, sem incluir produtos de outras categorias

### Requirement: Exibição de produtos reais no catálogo
Quando houver produtos no catálogo, a página inicial SHALL exibir um card para cada produto com nome, imagem indicada por URL, preço, descrição e categoria. Os dados SHALL corresponder a produtos reais pesquisados com autorização da pessoa usuária e SHALL NOT ser inventados ou substituídos por produtos demonstrativos. Cada produto SHALL registrar a URL de sua página de origem no arquivo JSON local.

#### Scenario: Visitante abre um catálogo com produtos cadastrados
- **WHEN** a fonte local contém produtos reais com páginas de origem registradas
- **THEN** a página inicial exibe os produtos com nome, imagem, preço, descrição e categoria correspondentes aos dados cadastrados

#### Scenario: Catálogo não contém produtos
- **WHEN** a fonte local não contém produtos cadastrados
- **THEN** a página inicial mantém uma mensagem clara de catálogo vazio e não exibe cards de produto

### Requirement: Navegação por categoria com produtos disponíveis
Quando o catálogo contiver produtos, a página inicial SHALL permitir selecionar uma categoria pelo menu lateral e SHALL exibir somente os produtos pertencentes à categoria selecionada. O visitante SHALL poder retornar à visualização de todos os produtos.

#### Scenario: Visitante seleciona uma categoria com produtos
- **WHEN** o visitante seleciona uma categoria no menu lateral
- **THEN** o catálogo exibe somente os produtos associados à categoria selecionada

#### Scenario: Visitante retorna à listagem completa
- **WHEN** o visitante seleciona a opção para ver todos os produtos
- **THEN** o catálogo exibe novamente todos os produtos cadastrados

### Requirement: Detalhes do produto em pop-up
Quando um produto do catálogo for ativado, a página inicial SHALL exibir um pop-up com imagem, nome, categoria, preço, descrição e especificações técnicas do produto selecionado. As especificações SHALL corresponder aos dados cadastrados para o produto e SHALL NOT ser inventadas. O pop-up SHALL informar que preços e disponibilidade podem mudar e devem ser confirmados na loja. O pop-up SHALL NOT oferecer link ou ação para abrir a loja.

#### Scenario: Visitante abre os detalhes de um produto
- **WHEN** o visitante ativa um card de produto
- **THEN** é exibido um pop-up com os detalhes do produto correspondente, sem alterar a seleção de categoria do catálogo

#### Scenario: Especificações variam conforme o produto
- **WHEN** o pop-up é exibido para um produto
- **THEN** as especificações cadastradas para esse produto são apresentadas como informações legíveis, sem exigir os mesmos campos técnicos para todas as categorias

#### Scenario: Produto não possui especificações adicionais cadastradas
- **WHEN** o pop-up é exibido para um produto sem especificações técnicas cadastradas
- **THEN** a interface informa que não há especificações adicionais disponíveis e não inventa valores

#### Scenario: Visitante fecha os detalhes
- **WHEN** o pop-up está aberto e o visitante aciona o botão de fechar, pressiona Escape ou ativa a área externa
- **THEN** o pop-up é fechado e o visitante retorna ao catálogo que estava visualizando

#### Scenario: Visitante consulta os detalhes em uma tela estreita
- **WHEN** o pop-up é aberto em uma tela estreita com conteúdo maior que a área visível
- **THEN** o conteúdo permanece legível e pode ser rolado dentro do pop-up sem causar rolagem horizontal da página

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
