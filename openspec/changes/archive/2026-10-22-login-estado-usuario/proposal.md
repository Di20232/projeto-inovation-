# Proposal: Exibir nome do usuário logado e redirecionar para a home

## Contexto
Atualmente, após realizar o login com sucesso em `/login`, o usuário recebe apenas uma mensagem de sucesso na própria página de login. O botão de login na barra superior da página inicial continua exibindo "Login" estaticamente, sem refletir que o usuário está autenticado.

## Objetivo
1. Armazenar o estado de autenticação e o nome/e-mail do usuário logado (usando um estado global ou compartilhado no Reflex).
2. Redirecionar automaticamente para a página inicial (`/`) após um login bem-sucedido.
3. Na barra superior da página inicial, exibir o nome do usuário logado (ou parte do e-mail) no lugar do botão "Login", com opção de sair (logout).

## Escopo
- Criar ou atualizar o estado de sessão (`AuthState` ou integrar com `LoginState`).
- Ajustar a ação de login para atualizar o usuário autenticado e navegar para `/`.
- Condicionar a renderização do botão de login/usuário na barra superior da página inicial (`index`).
- Criar a especificação, design e tarefas no OpenSpec.
