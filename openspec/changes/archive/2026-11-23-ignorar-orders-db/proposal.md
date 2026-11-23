# Proposta: Tirar o `orders_db.json` do git

## Contexto
O `orders_db.json` guarda pedidos com e-mail de clientes e estava versionado.

## Objetivo
Manter o arquivo só localmente.

## Escopo
- Adicionar `orders_db.json` ao `.gitignore` e removê-lo do índice com `git rm --cached` (o arquivo local é mantido).

## Observação
Quem fizer `git pull` deste commit numa cópia que ainda versionava o arquivo terá o `orders_db.json` apagado do disco; guarde uma cópia antes. O histórico do GitHub ainda tem versões antigas, apenas com e-mails `@exemplo.com`.
