# Design: Proteção de Autenticação no Checkout

## Arquitetura e Decisões
- **Estado**: Adicionado `redirect_after_login` em `AuthState`.
- **Eventos**:
  - `CatalogState.proceed_to_checkout`: Verifica se `AuthState.is_logged_in` é True. Se falso, define `redirect_after_login = "/pagamento"` e redireciona para `/login`; caso contrário, redireciona para `/pagamento`.
  - `LoginState.login`: Após sucesso no login, lê `redirect_after_login`, limpa-o e redireciona o usuário para o destino pretendido.
- **Segurança de Rota**: `checkout_page` valida `AuthState.is_logged_in`, exibindo tela de identificação necessária caso contrário.
