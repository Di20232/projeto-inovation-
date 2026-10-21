## Context

Consulte `proposal.md` para a motivação e `specs/identidade-inicial-loja/spec.md` para o comportamento esperado. A página atual é uma única tela Reflex em `/`, sem dados de produtos ou navegação por categorias.

## Goals / Non-Goals

**Goals:**
- Integrar a abertura do menu à identidade visual escura e roxa já estabelecida.
- Manter a página inicial como ponto de entrada, sem introduzir rotas de categoria enquanto não houver catálogo.
- Tratar o menu como uma navegação temporariamente indisponível, com os estados “Em breve” visíveis.

**Non-Goals:**
- Cadastrar, carregar ou integrar produtos.
- Filtrar produtos, criar páginas de categoria ou definir a futura organização do catálogo.
- Adicionar dependências ou alterar APIs, banco de dados ou Xano.

## Decisions

1. **Usar uma gaveta lateral sobreposta à página.** Um painel sobreposto, acompanhado de uma camada de fundo, mantém a tela inicial existente no lugar e deixa claro como voltar a ela. Uma barra permanentemente visível foi descartada por ocupar espaço na página e não corresponder ao comportamento deslizante solicitado.
2. **Manter a interação local à página inicial.** A gaveta abre sem mudar a rota; não existem destinos de categoria nesta etapa. A abertura e o fechamento podem ser controlados pelo estado local do app Reflex, sem uma nova camada de navegação ou dependência.
3. **Mostrar as quatro categorias acordadas como indisponíveis.** Computadores, Componentes, Periféricos e Acessórios aparecem com o rótulo “Em breve” e sem ação de navegação enquanto não houver produtos. Isso evita destinos vazios ou conteúdo fictício.
4. **Cobrir interações por mouse e teclado.** A gaveta deve ter um nome acessível, um controle explícito de fechar e fechamento pela tecla Escape e pela camada externa. Ao fechar, o foco deve retornar ao controle que abriu o menu; ao abrir, deve ser direcionado para dentro da gaveta.
5. **Adaptar a largura ao espaço disponível.** Em telas estreitas, a gaveta deve caber na viewport sem criar rolagem horizontal; em telas amplas, permanece um painel lateral de largura limitada.

## Risks / Trade-offs

- [Categorias marcadas “Em breve” podem parecer navegáveis] → Exibir o estado junto a cada categoria e não oferecer ação que sugira resultados existentes.
- [A camada sobreposta pode dificultar a navegação por teclado ou leitor de tela] → Usar semântica acessível, ordem de foco previsível, Escape para fechar e retorno do foco ao acionador.
- [O painel pode exceder a largura disponível em telas estreitas] → Limitar sua largura à viewport e verificar a ausência de rolagem horizontal.

## Migration Plan

Não há migração de dados nem alteração de rotas. A mudança pode ser revertida removendo o controle e o estado da gaveta da página inicial.
