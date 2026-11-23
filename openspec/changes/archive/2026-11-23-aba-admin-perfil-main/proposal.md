# Proposta: Aba "Gerenciar Site" no main

## Contexto
Ao logar como administrador, o `/perfil` não mostrava a aba "Gerenciar Site". O código da aba existia só na branch `claude/painel-administrativo` (17/11), que nunca foi mesclada no `main`; o `main` tinha apenas a página `/admin`, sem checagem de login.

## Objetivo
Levar a aba administrativa ao `main` e garantir que o privilégio de admin não sobreviva ao logout.

## Escopo
- Mesclar `claude/painel-administrativo` no `main` (sem conflitos).
- Zerar `is_admin` e sair da aba admin em `AuthState.confirm_logout`.

## Fora do escopo
- Edição de produto (change `edicao-produto-painel`).
