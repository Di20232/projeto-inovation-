# Design: Exibir nome do usuário logado e redirecionar para a home

## Estado de Sessão
Criar um `AuthState` (herdando de `rx.State`) contendo:
- `is_logged_in: bool = False`
- `user_name: str = ""`
- `user_email: str = ""`

## Ação de Login
No método `login` de `LoginState` (ou integrado com `AuthState`):
- Ao validar com sucesso as credenciais (ou resposta positiva do Xano/mock):
  - Definir `AuthState.is_logged_in = True`
  - Definir `AuthState.user_name` com o nome extraído ou o prefixo do e-mail (ex: antes do `@`).
  - Redirecionar com `return rx.redirect("/")`.

## Barra Superior da Página Inicial (`index`)
Substituir o link fixo "Login" por uma condição baseada em `AuthState.is_logged_in`:
- Se **falso**: exibe o botão/link "Login" apontando para `/login`.
- Se **verdadeiro**: exibe um componente (botão ou menu) com o nome do usuário e opção de logout (que reseta o estado e recarrega).
