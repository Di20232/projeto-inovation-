## ADDED Requirements

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
