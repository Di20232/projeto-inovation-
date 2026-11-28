# Proposta: Hash do admin no `.env.example`

## Contexto
Em outra máquina, o painel administrativo não aparecia. O `.env.example` trazia uma senha em texto puro em `ADMIN_PASSWORD_HASH`, e o app só aceita o hash PBKDF2, então o login do admin era recusado.

## Objetivo
Quem copiar o exemplo saber que precisa gerar o hash.

## Escopo
- Deixar `ADMIN_PASSWORD_HASH` vazio e explicar no comentário como gerar, onde colar e onde o painel aparece.

## Fora do escopo
- Alterar o `.env` já existente em cada máquina.
