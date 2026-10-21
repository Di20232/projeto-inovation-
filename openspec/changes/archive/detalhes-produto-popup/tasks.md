## 1. Dados de especificações

- [x] 1.1 Adicionar ao modelo do produto e ao JSON um campo de especificações técnicas flexível por rótulo e valor; cadastrar apenas informações confirmadas para cada item e verificar a validação de dados ausentes ou inválidos.

## 2. Pop-up de detalhes

- [x] 2.1 Tornar cada card acionável e abrir um diálogo compartilhado com imagem, nome, categoria, preço, descrição e especificações do produto selecionado; verificar que os dados correspondem ao item ativado e que o aviso de preço variável não inclui link para a loja.
- [x] 2.2 Permitir fechar o diálogo pelo botão, por Escape e pela área externa, sem perder o filtro atual; verificar cada forma de fechamento e reabertura.
- [x] 2.3 Exibir uma mensagem quando não houver especificações adicionais e garantir que nenhum valor técnico fictício, link para loja, galeria, carrinho ou ação de compra seja apresentado.

## 3. Validação integrada

- [x] 3.1 Verificar legibilidade, rolagem interna e ausência de rolagem horizontal com o diálogo aberto em telas estreitas e amplas.
- [x] 3.2 Executar `reflex compile --dry` e `openspec validate --strict`; confirmar que a listagem e os filtros existentes continuam funcionando.
