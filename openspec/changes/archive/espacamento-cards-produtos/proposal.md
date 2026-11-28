## Why

Os cards do catálogo estão separados por apenas 12 pixels, deixando a composição visual muito compacta e dificultando a distinção individual de cada produto.

## What Changes

- Aumentar o espaçamento horizontal e vertical entre os cards do catálogo.
- Manter exatamente duas colunas de produtos em todas as larguras compatíveis com o layout atual.
- Preservar o tamanho das imagens e o comportamento existente de detalhes e navegação dos cards.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-inicial-loja`: Ajustar o espaçamento visual dos cards de produtos reais sem alterar o número de duas colunas.

## Impact

- Layout do catálogo em `python/python.py`.
- Sem alterações em dados, APIs, componentes de estado, rotas ou dependências.
