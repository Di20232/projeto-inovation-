## Context

O catálogo já usa `rx.grid` com duas colunas e a propriedade `gap="12px"`. A alteração solicitada é exclusivamente visual e não requer mudança nos dados ou no estado da aplicação.

## Goals / Non-Goals

**Goals:**
- Criar uma separação um pouco maior entre os cards.
- Preservar duas colunas de produtos no catálogo.
- Manter a largura total disponível e o comportamento dos cards.

**Non-Goals:**
- Alterar o número de colunas para outro formato responsivo.
- Alterar imagens, conteúdo, filtros, ações ou detalhes dos produtos.
- Introduzir novas dependências ou estilos globais.

## Decisions

- Aumentar o `gap` da grade e manter `columns="2"`.
- Usar um espaçamento uniforme para as direções horizontal e vertical, evitando diferenças visuais entre linhas e colunas.
- Evitar alterar margens individuais dos cards para não duplicar ou quebrar o alinhamento da grade.

## Risks / Trade-offs

- [Espaçamento excessivo reduz a área útil dos cards] → Usar uma distância pequena e verificar visualmente o catálogo.
- [Largura estreita comprime os cards] → Preservar o layout existente de duas colunas e validar que não surge rolagem horizontal.

## Migration Plan

- Ajustar a propriedade de espaçamento da grade.
- Compilar o aplicativo e reiniciar o servidor em produção.
- Reverter apenas o valor do `gap` caso o resultado visual não seja adequado.
