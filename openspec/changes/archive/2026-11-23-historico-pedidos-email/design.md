# Design

- `order_persistence.load_orders_for_email(email)`: filtra sem diferenciar maiúsculas, mais recente primeiro; pedidos sem `user_email` não aparecem; arquivo ausente/corrompido vira lista vazia.
- `AuthState._refresh_orders()`: junta pedidos do arquivo com os que existem só na sessão (ex.: aceitos pelo Xano). Evento `load_my_orders` no `on_load` do `/perfil`.
- Login e cadastro zeram `orders` antes de carregar; `confirm_logout` zera `orders`.
- Pedido novo entra no topo da lista.
- Commit: `55ca8ca`.
