# Spec: Checkout e número do pedido

## Requisitos
- Sem `ASAAS_API_KEY`, acessando por localhost, o checkout cria o pedido sem cobrança e sem pedir cartão.
- Fora de localhost, sem chave, o pedido é recusado com mensagem.
- Após finalizar, o cliente vê o número do pedido (`#NF-…`) na confirmação e o mesmo número em "Meus Pedidos".
