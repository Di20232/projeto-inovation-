# Design: Página de Perfil do Usuário

## Arquitetura e Decisões
- **Estado**: Adicionados campos e eventos em `AuthState` (`user_phone`, `profile_message`, `update_profile`).
- **Componentes**:
  - `profile_page`: Rota `/perfil` exibindo informações do usuário logado, formulário de edição de nome, e-mail (somente leitura) e guard de acesso restrito.
  - Link no cabeçalho sobre o nome do usuário apontando para `/perfil`.
