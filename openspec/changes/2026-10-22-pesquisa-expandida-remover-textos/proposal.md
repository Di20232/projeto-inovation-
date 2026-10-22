# Proposal: Remover textos introdutórios e dinamizar a barra de pesquisa

## Contexto
O usuário solicitou remover os textos introdutórios ("Tecnologia para ir além..." e subtítulos), colocar a barra de pesquisa no topo (acima das colunas de categorias e produtos) e fazer com que ela aumente de tamanho (expanda suavemente) ao ser clicada ou focar.

## Objetivo
1. Remover os títulos e descrições de introdução da página inicial.
2. Posicionar a barra de pesquisa no topo do layout principal.
3. Aplicar estilo e transição CSS com aumento de largura (`scale` ou largura flexível/transição de width) ao receber foco (`_focus`).

## Escopo
- Atualizar a função `index` em `python/python.py`.
- Atualizar a função `product_catalog` para reposicionar a barra de pesquisa no topo.
- Adicionar propriedades de transição e animação no foco do componente `rx.input`.
- Registrar a change no OpenSpec.
