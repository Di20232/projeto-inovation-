 ## 1. Fonte local de produtos

- [x] 1.1 Criar a estrutura `python/catalog.json` com os campos acordados, incluindo URL de origem, e validar a leitura dos dados e a rejeição explícita de estruturas inválidas.
- [x] 1.2 Cadastrar um produto real pesquisado para cada categoria com autorização da pessoa usuária; verificar que cada item tem nome, URL de imagem, preço, descrição, categoria e fonte e que nenhum produto foi inventado.

## 2. Catálogo e categorias

- [x] 2.1 Carregar os produtos do JSON e renderizar cards com nome, imagem, preço, descrição e categoria; verificar que o conteúdo exibido corresponde aos dados de origem.
- [x] 2.2 Tornar o menu lateral um filtro funcional para categorias com produtos e manter “Em breve” nas categorias sem itens; verificar os resultados de cada categoria e a opção “Todos”.
- [x] 2.3 Preservar uma mensagem de catálogo vazio quando a fonte não tiver produtos e executar `reflex compile --dry`; verificar os estados vazio e preenchido sem produtos fictícios.

## 3. Validação integrada

- [x] 3.1 Validar visualmente os cards e filtros em telas estreitas e amplas, confirmando legibilidade e ausência de rolagem horizontal.
