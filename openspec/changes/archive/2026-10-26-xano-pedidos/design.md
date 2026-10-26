# Design: Integração de Pedidos com Xano

## Arquitetura e Decisões
- **Script de Teste**: `test_xano_orders.py` utiliza `httpx` para enviar dados de pedido estruturados para o endpoint `/orders` do Xano.
- **Payload**: Inclui dados do cliente, lista de itens do carrinho, valores monetários formatados e endereço de entrega validado via CEP.
