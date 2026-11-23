# Spec: Endereço de entrega no checkout

## Requisitos
- O pedido só é confirmado com CEP de 8 dígitos, endereço, número, bairro, cidade e UF de 2 letras preenchidos.
- Faltando algum desses, o checkout mostra quais campos faltam e não cria pedido.
- Complemento é opcional.
