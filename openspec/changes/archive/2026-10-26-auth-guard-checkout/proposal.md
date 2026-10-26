# Proposta: Proteção de Autenticação no Checkout (Auth Guard)

## Contexto
O usuário solicitou que, antes de prosseguir para a página de pagamento (`/pagamento`), o sistema verifique se a conta está logada. Caso contrário, o usuário deve ser redirecionado para o login e, após autenticar-se com sucesso, retornado automaticamente para a tela de pagamento.

## Objetivo
Implementar a verificação de autenticação no botão de checkout do carrinho e na própria página de pagamento, guardando a URL de retorno (`redirect_after_login`) no estado global de autenticação (`AuthState`) e redirecionando o usuário para `/login` quando não autenticado.

## Escopo
- Adicionar `redirect_after_login` em `AuthState`.
- Criar evento `proceed_to_checkout` em `CatalogState` para verificar `AuthState.is_logged_in`.
- Atualizar `LoginState.login` para redirecionar para `redirect_after_login` (ou `/` por padrão).
- Atualizar `checkout_page` para exibir aviso de acesso restrito caso o usuário acesse `/pagamento` diretamente sem login.
