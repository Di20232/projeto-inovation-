## Context

O app atual é uma aplicação Reflex mínima com uma única página em `/`. Consulte `proposal.md` para a motivação e `specs/identidade-inicial-loja/spec.md` para o comportamento esperado.

## Goals / Non-Goals

**Goals:**
- Manter a aplicação e a página inicial no Reflex, sem alterar o ponto de entrada nem criar uma arquitetura adicional.
- Estabelecer hierarquia visual simples: marca, mensagem curta de apresentação e estado vazio do catálogo.
- Usar fundo quase preto, superfícies escuras e roxo como destaque; reservar texto de alto contraste para informações essenciais.

**Non-Goals:**
- Criar produtos, preços, categorias funcionais, busca, filtros ou ações de compra.
- Adicionar rotas, persistência, APIs, dependências ou integração com Xano.
- Definir agora a identidade visual completa da futura loja.

## Decisions

1. **Evoluir a única página existente.** Reutilizar o ponto de entrada Reflex atual e manter a rota `/`, evitando adicionar navegação ou componentes de aplicação sem necessidade para o estado inicial.
2. **Compor a tela apenas com blocos de apresentação.** Usar uma área superior com o nome NightFall e uma seção principal com mensagem de boas-vindas e estado vazio. A alternativa de desenhar cards de catálogo desabilitados foi rejeitada porque poderia sugerir produtos cadastrados.
3. **Usar uma paleta local e pequena.** Como ponto de partida, usar fundo próximo de `#0B0B12`, superfícies próximas de `#151321`, roxo de destaque próximo de `#8B5CF6` e texto claro. Ajustar cores finais para manter contraste legível; não introduzir sistema global de temas nesta etapa.
4. **Manter layout fluido e centralizado.** Limitar a largura do conteúdo em telas amplas e permitir que marca e mensagem se reorganizem em telas estreitas, sem rolagem horizontal. Não adicionar biblioteca de UI nem imagens de produto.
5. **Manter conteúdo estático enquanto não há catálogo.** A mensagem de estado vazio será apresentada sem consultar dados, já que não há fonte de produtos aprovada para esta primeira tela.

## Risks / Trade-offs

- [Roxo luminoso sobre preto pode ter contraste insuficiente em textos pequenos] → Usar roxo como destaque decorativo e manter textos essenciais em tons claros, verificando contraste visual.
- [Uma tela intencionalmente vazia pode parecer incompleta] → Explicar explicitamente que o catálogo está sendo preparado e não renderizar elementos falsos de compra.
- [Uma composição desktop pode ficar apertada em telas pequenas] → Validar a página em larguras estreitas e amplas antes de concluir a mudança.

## Migration Plan

Não há migração de dados. Substituir a mensagem provisória atual pela interface NightFall e manter a rota inicial. Se a identidade ou o catálogo forem conectados a dados em outra etapa, especificar essa integração em uma change separada.
