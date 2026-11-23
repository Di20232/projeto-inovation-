# Proposta: Checkout em Modo Simulado e Número do Pedido

## Contexto
Sem `ASAAS_API_KEY` não havia como fechar um pedido para testar o fluxo. Além disso, ao finalizar, o cliente via apenas o ID da cobrança no Asaas, e não o número do pedido.

## Objetivo
Permitir testar pedidos localmente sem cobrança e mostrar ao cliente o número real do pedido.

## Escopo
- Modo simulado: sem `ASAAS_API_KEY` e com acesso por localhost, o pedido é criado sem cobrança (pode ser desligado com `NIGHTFALL_SIMULATED_PAYMENTS=0`).
- Quadro de confirmação com o número `#NF-…`, total, status e atalho para "Meus Pedidos" (fluxo real e simulado).
- Corrigir a data exibida com aspas em "Meus Pedidos".
