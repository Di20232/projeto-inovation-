# Especificação: Proteção de Autenticação no Checkout

## Requisitos
1. **Verificação Pré-Checkout**: Ao clicar em "Ir para o Pagamento" no carrinho, o sistema deve verificar se o usuário está autenticado (`is_logged_in`).
2. **Redirecionamento para Login**: Caso o usuário não esteja logado, ele deve ser redirecionado para `/login` e a rota `/pagamento` deve ser salva como destino de retorno (`redirect_after_login`).
3. **Retorno Automático**: Após realizar o login com sucesso, o usuário deve ser redirecionado de volta para a página de pagamento (`/pagamento`).
4. **Proteção de Rota Direta**: Caso o usuário acesse `/pagamento` diretamente sem login, a página deve exibir uma mensagem de acesso restrito solicitando identificação.
