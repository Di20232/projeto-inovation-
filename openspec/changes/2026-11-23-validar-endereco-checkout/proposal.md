# Proposta: Validar Endereço no Checkout

## Contexto
Em 2026-11-23 o checkout simulado confirmou o pedido `#NF-9C7A4738` com todos os campos de endereço em branco. O fluxo com cartão (Asaas) também não confere o endereço.

## Objetivo
Não confirmar pedido sem endereço de entrega.

## Escopo
- Antes de criar o pedido (fluxo simulado e fluxo com cartão), exigir CEP com 8 dígitos, endereço, número, bairro, cidade e UF com 2 letras. Complemento continua opcional.
- Mostrar no checkout quais campos faltam.

## Fora do escopo
- Gravar o endereço no pedido (`orders_db.json`/Xano).
