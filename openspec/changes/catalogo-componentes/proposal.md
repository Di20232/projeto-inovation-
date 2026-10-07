## Why

Quem visita uma loja de componentes precisa descobrir quais peças estão disponíveis e comparar informações básicas antes de decidir o que comprar. O projeto ainda apresenta somente a página padrão do Reflex; um catálogo público é o primeiro fluxo útil da loja e permite validar sua navegação sem exigir cadastro.

## What Changes

- Substituir a página inicial de boas-vindas por uma vitrine pública de componentes de computador.
- Organizar os produtos por categorias e permitir a navegação entre elas.
- Exibir em cada produto imagem, nome, marca, preço e disponibilidade para comparação.
- Disponibilizar uma página ou visualização de detalhes com a imagem e as especificações do produto.
- Usar dados de exemplo no escopo inicial, sem depender de uma fonte externa ou persistência de catálogo.
- Associar a cada produto de demonstração uma URL pública de imagem.
- Manter a navegação e a visualização dos produtos acessíveis sem login.

## Capabilities

### New Capabilities
- `catalogo-componentes`: navegação pública por categorias, listagem de produtos e consulta dos detalhes de um produto.

### Modified Capabilities
- Nenhuma.

## Impact

- A página e o estado da aplicação em `python/python.py`.
- Nova especificação de comportamento em `openspec/changes/catalogo-componentes/specs/catalogo-componentes/spec.md`.
- Sem novas dependências, APIs externas ou persistência nesta Change.
- As imagens de demonstração são carregadas de URLs públicas externas.
- Busca avançada, filtros, carrinho, autenticação, checkout e administração de catálogo ficam fora do escopo.
