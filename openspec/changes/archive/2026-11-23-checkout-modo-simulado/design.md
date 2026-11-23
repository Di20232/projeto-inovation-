# Design

- `simulated_payments_enabled()` e `LOCAL_HOSTNAMES`.
- `_register_order(...)`: caminho único (real e simulado) que grava no Xano/`orders_db.json` (agora com `user_email`), atualiza `AuthState.orders`, guarda `last_order_*` e limpa o carrinho.
- `_finalize_simulated_order()`: exige login, carrinho, origem localhost e total > 0.
- UI: aviso amarelo no lugar do formulário de cartão; botão "Confirmar Pedido (simulado)"; `order_confirmation_banner()` no `/pagamento`.
- Data: `order["date"].to(str)` em vez de `.to_string()`.
- Commit: `5002e61`.
