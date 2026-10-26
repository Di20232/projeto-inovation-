# Tarefas: Proteção de Autenticação no Checkout

- [x] 1. Adicionar campo `redirect_after_login` em `AuthState`.
- [x] 2. Implementar evento `proceed_to_checkout` em `CatalogState` verificando `is_logged_in`.
- [x] 3. Atualizar fluxo de login em `LoginState.login` para respeitar `redirect_after_login`.
- [x] 4. Atualizar botão do carrinho para chamar `proceed_to_checkout`.
- [x] 5. Adicionar guard de autenticação na `checkout_page`.
- [x] 6. Verificar compilação com `reflex compile --dry`.
