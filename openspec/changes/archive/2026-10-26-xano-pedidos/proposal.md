# Proposta: Integração de Pedidos com Xano Backend

## Contexto
O projeto utiliza o Xano como backend para autenticação (`/signup`), mas faltava a estrutura e o script de validação para persistência de pedidos (`/orders`).

## Objetivo
Criar script de teste e integração (`test_xano_orders.py`) para enviar o payload completo do pedido (itens, subtotal, frete, desconto, endereço de entrega e método de pagamento) para o backend Xano.

## Escopo
- Script `test_xano_orders.py` simulando envio de pedido para o endpoint Xano `/orders`.
- Documentação da estrutura de dados de pedidos esperada pelo backend Xano.
