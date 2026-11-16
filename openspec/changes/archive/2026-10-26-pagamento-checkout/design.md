# Design: Tela de Pagamento e Checkout

## Arquitetura e Decisões
- **Estado**: Adicionados campos de endereço de entrega (`shipping_cep`, `shipping_address`, `shipping_number`, `shipping_complement`, `shipping_neighborhood`, `shipping_city`, `shipping_state`), campos de pagamento (`payment_method`, `card_number`, `card_name`, `card_expiry`, `card_cvv`), e estado de conclusão (`order_success`, `order_id`) a `CatalogState` em `python/python.py`.
- **Componentes**:
  - `checkout_page`: Rota `/pagamento` contendo o formulário de endereço e seleção de forma de pagamento, com resumo do pedido à direita.
  - Tela de sucesso de pedido com número gerado aleatoriamente e botão para retornar à loja.
- **Formatação de Moeda e Estilo**: Cores consistentes com o tema escuro NightFall (`#0b0b12`, roxo e violeta).
