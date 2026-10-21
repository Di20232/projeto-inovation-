## Context

Consulte `proposal.md` para a motivação e `specs/identidade-inicial-loja/spec.md` para o comportamento esperado. Os cards são renderizados a partir de `python/catalog.json` e já existe um diálogo controlado para o menu de categorias.

## Goals / Non-Goals

**Goals:**
- Manter os detalhes no catálogo e usar uma única apresentação de pop-up para todos os produtos.
- Permitir especificações em pares de rótulo e valor adequados a cada item, sem exigir um esquema técnico uniforme entre categorias.
- Preservar uma experiência utilizável por teclado e em telas pequenas.

**Non-Goals:**
- Criar páginas individuais para os produtos ou navegação para as lojas de origem.
- Adicionar galeria de imagens, carrinho, checkout ou ações de compra.
- Buscar especificações dinamicamente em APIs externas.

## Decisions

1. **Registrar as especificações como dados do produto em `catalog.json`.** Cada produto terá uma coleção de campos de especificação em formato rótulo/valor, que pode variar entre categorias. Isso mantém os dados explícitos e evita deduzir atributos a partir de textos ou inventar informações. Um produto sem especificações adicionais continuará válido e terá um estado informativo no pop-up.
2. **Usar um diálogo único controlado pela seleção atual.** Ativar um card seleciona aquele produto e abre o diálogo compartilhado; fechar limpa a seleção sem alterar a categoria do catálogo. Isso evita manter diálogos independentes para cada card e mantém uma única experiência acessível.
3. **Manter os elementos existentes do card como resumo.** O pop-up complementa a listagem com os detalhes do item, enquanto a lista e seus filtros permanecem no lugar ao abrir e fechar. O aviso sobre a variação de preço e disponibilidade será textual, sem link ou ação para a loja.
4. **Permitir rolagem vertical dentro do diálogo.** Limitar a área do pop-up à viewport e rolar seu conteúdo quando necessário evita cortar especificações em telas estreitas; o diálogo deve evitar overflow horizontal.

## Risks / Trade-offs

- [Especificações podem ser incompletas ou incorretas] → Cadastrar somente valores confirmados para cada item; omissões aparecem como não disponíveis, nunca como conteúdo fictício.
- [Conteúdo longo pode exceder a tela em dispositivos móveis] → Restringir as dimensões do diálogo à viewport e permitir rolagem interna.
- [A seleção pode ficar dessincronizada com o diálogo] → Centralizar a abertura e o fechamento no estado do produto selecionado e verificar retorno ao catálogo após cada forma de fechamento.

## Migration Plan

Adicionar a coleção de especificações aos dados dos produtos existentes, atualizar o carregamento e validação dos dados e então conectar a ativação dos cards ao diálogo de detalhes. Se for necessário reverter, remover a interação e o diálogo e retirar o campo opcional de especificações sem alterar nome, imagem, preço, descrição, categoria ou fonte dos produtos.
