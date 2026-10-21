## Context

Consulte `proposal.md` para a motivação e `specs/identidade-inicial-loja/spec.md` para os critérios visuais e funcionais. O menu lateral atual é um diálogo controlado, com cabeçalho, opções de categorias e filtro aplicado ao catálogo.

## Goals / Non-Goals

**Goals:**
- Reutilizar o diálogo e o estado existentes, limitando a mudança à apresentação do menu.
- Manter a identidade escura e roxa da NightFall com melhor hierarquia, respiro e indicação da opção selecionada.
- Manter as opções utilizáveis por toque e teclado em diferentes larguras.

**Non-Goals:**
- Alterar a lista de categorias, regras de disponibilidade ou comportamento dos filtros.
- Adicionar ícones, contadores de produtos, animações complexas ou uma biblioteca visual.
- Carregar fontes ou outros recursos de terceiros.

## Decisions

1. **Usar uma pilha de fontes de sistema com fallbacks.** Aplicar uma pilha sans-serif com Inter quando instalada, seguida por `ui-sans-serif`, `system-ui` e `Segoe UI`. Isso dá aparência contemporânea sem requisição externa, dependência nova ou falha de carregamento. Alternativas consideradas: baixar/empacotar uma fonte, que aumenta manutenção, ou buscar Inter no Google Fonts, que depende da rede.
2. **Criar ritmo visual com espaçamento e hierarquia, sem mudar o conteúdo.** Dar separação mais clara entre cabeçalho e lista; usar linhas de categoria com altura e padding confortáveis, tipografia consistente e estados de foco/hover coerentes com o tema. Preservar rótulos e estado “Em breve”.
3. **Derivar o destaque visual da seleção existente.** A opção correspondente a `selected_category` deve receber tratamento visual ativo, incluindo “Todos os produtos” quando aplicável. Isso evita estado paralelo que poderia divergir do filtro real.
4. **Preservar o diálogo acessível e responsivo.** Manter acionadores e fechamento atuais, Escape e área externa, além de dimensionamento e rolagem vertical para telas estreitas; estilos não devem introduzir overflow horizontal.

## Risks / Trade-offs

- [Uma pilha de fontes depende das fontes disponíveis em cada dispositivo] → Incluir fallbacks amplos e manter a hierarquia baseada em tamanho, peso e espaçamento, não em uma face específica.
- [Estados visuais mais ricos podem reduzir contraste ou confundir foco com seleção] → Preservar contraste do tema e distinguir estados ativo, hover e foco com tratamentos compatíveis.
