# Proposta: Tela de Pagamento e Checkout na Vitrine NightFall

## Contexto
O usuário precisa de uma experiência completa de conclusão de compra (checkout) após adicionar produtos ao carrinho e acessar a página de carrinho (`/carrinho`).

## Objetivo
Implementar a página dedicada de checkout (`/pagamento`) na aplicação Reflex (`python/python.py`), permitindo preencher endereço de entrega (CEP, estado, rua, número, bairro, cidade), selecionar a forma de pagamento (Cartão de Crédito, Pix, Boleto), preencher dados de pagamento correspondentes, confirmar o pedido e visualizar a tela de sucesso com número do pedido gerado.

## Escopo
- Rota dedicada `/pagamento` com layout responsivo em duas colunas (formulário de entrega/pagamento e resumo do pedido).
- Seleção interativa de métodos de pagamento (Cartão com validações, Pix com QR code simulado e chave copia/cola, Boleto bancário).
- Estado reativo de checkout em `CatalogState`.
- Confirmação de pedido com limpeza de carrinho, geração de ID de pedido e exibição de tela de sucesso.
