## ADDED Requirements

### Requirement: Exibição de produtos reais no catálogo
Quando houver produtos no catálogo, a página inicial SHALL exibir um card para cada produto com nome, imagem indicada por URL, preço, descrição e categoria. Os dados SHALL corresponder a produtos reais pesquisados com autorização da pessoa usuária e SHALL NOT ser inventados ou substituídos por produtos demonstrativos. Cada produto SHALL registrar a URL de sua página de origem no arquivo JSON local.

#### Scenario: Visitante abre um catálogo com produtos cadastrados
- **WHEN** a fonte local contém produtos reais com páginas de origem registradas
- **THEN** a página inicial exibe os produtos com nome, imagem, preço, descrição e categoria correspondentes aos dados cadastrados

#### Scenario: Catálogo não contém produtos
- **WHEN** a fonte local não contém produtos cadastrados
- **THEN** a página inicial mantém uma mensagem clara de catálogo vazio e não exibe cards de produto

### Requirement: Navegação por categoria com produtos disponíveis
Quando o catálogo contiver produtos, a página inicial SHALL permitir selecionar uma categoria pelo menu lateral e SHALL exibir somente os produtos pertencentes à categoria selecionada. O visitante SHALL poder retornar à visualização de todas as categorias ou de todos os produtos.

#### Scenario: Visitante seleciona uma categoria com produtos
- **WHEN** o visitante seleciona uma categoria no menu lateral
- **THEN** o catálogo exibe somente os produtos associados à categoria selecionada

#### Scenario: Visitante retorna à listagem completa
- **WHEN** o visitante seleciona a opção para ver todos os produtos
- **THEN** o catálogo exibe novamente todos os produtos cadastrados

## MODIFIED Requirements

### Requirement: Categorias indisponíveis enquanto o catálogo está vazio
Enquanto não houver produtos disponíveis na respectiva categoria, ela SHALL ser identificada com o estado “Em breve” e SHALL NOT permitir navegação para resultados inexistentes nem apresentar produtos fictícios. Quando houver produtos reais cadastrados em uma categoria, essa categoria SHALL permitir a filtragem do catálogo por seus produtos. Os campos de imagem e página de origem de cada produto SHALL conter URLs HTTP ou HTTPS válidas.

#### Scenario: Visitante consulta uma categoria antes da disponibilização do catálogo
- **WHEN** o menu é exibido e uma categoria não possui produtos cadastrados
- **THEN** a categoria sem produtos mostra “Em breve” e não indica resultados ou produtos disponíveis

#### Scenario: Visitante seleciona uma categoria disponível
- **WHEN** o menu é exibido e há produtos cadastrados em uma categoria
- **THEN** essa categoria pode ser selecionada para filtrar o catálogo, sem incluir produtos de outras categorias
