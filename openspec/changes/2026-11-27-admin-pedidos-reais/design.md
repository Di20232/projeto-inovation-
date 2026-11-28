# Design

- `order_persistence.load_all_orders` lê o `orders_db.json`.
- `AdminState.all_orders` é preenchida ao abrir `/admin` ou a aba "Pedidos", depois de conferir `is_admin` no servidor; no logout é esvaziada.
- Os dados vêm pela sessão do administrador, sem ficar escritos no JavaScript.
