## Context

A aplicação Reflex tem uma página inicial em `/` com identidade visual própria e um botão “Login”, mas ainda não tem uma página de login. Consulte `proposal.md` e `specs/login-screen/spec.md` para motivação e comportamento esperado.

## Goals / Non-Goals

**Goals:**
- Adicionar a rota `/login` seguindo a estrutura de páginas Reflex já usada pela aplicação.
- Manter navegação simples e coerente com a interface existente.
- Isolar a experiência à apresentação visual, sem estado de autenticação ou tratamento de credenciais.

**Non-Goals:**
- Autenticar usuários, validar credenciais ou implementar recuperação/cadastro de conta.
- Enviar, armazenar ou persistir dados, ou integrar banco de dados e APIs.

## Decisions

- Registrar a tela como uma página Reflex na rota `/login`, em vez de abrir um diálogo na página inicial. Uma rota própria atende ao destino solicitado e pode ser acessada diretamente.
- Usar um link estilizado como botão na página inicial para navegar até `/login` e um link de retorno para `/`. Isso aproveita navegação declarativa, sem adicionar um manipulador de evento para o botão de entrada.
- Compor a nova página com os componentes visuais nativos do Reflex e reutilizar cores, tipografia e espaçamentos da identidade NightFall. Campos e botão do formulário não terão manipuladores nem chamada de serviço; não será criada lógica de submissão.

## Risks / Trade-offs

- [Os controles podem parecer funcionais apesar de não autenticar] → Deixar explícito no escopo que o botão do formulário é apenas visual e não exibir sucesso ou erro de autenticação.
- [A rota pode divergir visualmente da página inicial] → Reutilizar a paleta e os padrões visuais já presentes na interface NightFall.

## Migration Plan

Não há migração de dados nem dependência nova. Registrar a página, conectar a navegação entre `/` e `/login`, e validar a compilação Reflex e a navegação/legibilidade das duas telas. Para reverter, remover a página `/login` e restaurar o botão inicial sem destino.
