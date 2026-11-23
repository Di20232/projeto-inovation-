# Design: Painel Administrativo Exclusivo

## Architecture & State
- **AuthState**: Adiciona `is_admin: bool`. No evento `LoginState.login`, se `email == "admin@admin.com"` e `password == "admin123"`, define `is_admin = True`.
- **CatalogState / AuthState**: Adiciona campos de estado para formulário de novo produto e edição de produtos existentes, além de eventos `add_product`, `update_product`, `delete_product`.
- **UI**: Na página `/perfil`, se `auth_state.is_admin` for verdadeiro, exibe o botão da aba "Gerenciar Site". O conteúdo da aba exibe a listagem de produtos com opções de edição rápida, formulário de adição de novo produto e gerenciamento de marcas.
