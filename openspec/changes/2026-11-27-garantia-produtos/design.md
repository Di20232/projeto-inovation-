# Design

## Dados
- `Product` e `CartItem` ganham `warranty_months: int`. Catálogo sem o campo continua válido e vale 0.
- O banco usado pelo app é `python/catalog.json` (produtos) e `orders_db.json` (pedidos). O envio ao Xano leva o campo junto, mas o endpoint de produtos respondia 404 em 2026-11-27.

## Cálculo (`warranty.py`)
- `parse_warranty_months`: valida o campo do painel; vazio vale 0.
- `add_months`: soma meses de calendário e ajusta o fim do mês.
- `load_warranties_for_email`: filtra os pedidos pelo e-mail, calcula a validade pela data do pedido. A garantia vale até o último dia, inclusive.
- O prazo gravado no pedido vale mais que o do catálogo. Pedidos antigos, sem o campo, usam o prazo atual do produto de mesmo nome.

## Interface
- `AuthState.warranties` é recarregada ao abrir `/perfil` e ao abrir a aba "Garantia"; o logout limpa a lista.
- `warranty_card` desenha cada item.

## Limitações
- Pedido aceito pelo Xano não é gravado em `orders_db.json`, portanto não entraria na aba.
- Pedidos em modo simulado também geram garantia.
- Se o catálogo vier do Xano sem o campo, os produtos ficam com 0.
