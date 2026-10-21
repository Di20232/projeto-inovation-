## Why

Com a identidade da NightFall e o menu lateral de categorias definidos, a página ainda não apresenta produtos reais para o visitante explorar. Este change permitirá exibir quatro produtos reais, um por categoria, pesquisados em lojas públicas e com as páginas de origem registradas, sem inventar produtos ou depender de uma API inexistente.

## What Changes

- Substituir o estado de catálogo em preparação por uma listagem de quatro produtos reais pesquisados, um por categoria.
- Exibir cards com nome, imagem por URL, preço, descrição e categoria.
- Usar um arquivo local JSON como fonte inicial dos dados, incluindo a URL da página de origem de cada produto, sem backend, API ou integração com Xano.
- Tornar as categorias existentes funcionais para filtrar os produtos exibidos.
- Manter um estado vazio informativo caso o arquivo não contenha produtos.

## Capabilities

### New Capabilities

### Modified Capabilities
- `identidade-inicial-loja`: atualizar o comportamento do catálogo vazio para permitir a listagem de produtos reais e a navegação por categoria.

## Impact

- Página inicial Reflex em `python/python.py`.
- Novo arquivo local de dados do catálogo em JSON, contendo quatro produtos reais pesquisados e suas fontes.
- Especificação existente em `openspec/specs/identidade-inicial-loja/`.
- Nenhuma API, banco de dados, dependência externa ou integração com Xano será adicionada.
