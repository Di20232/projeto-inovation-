# Proposta: Atualização dos Schemas de Tabelas e Endpoint de Cadastro no Backend

## Contexto
O front-end envia `cpf` e `birth_date` durante o cadastro do usuário, mas o schema da tabela `USER` (`table/user.xs`) e o endpoint de signup (`api/autentificacao/auth/signup_POST.xs`) não persistiam esses campos. Além disso, a tabela de endereços (`table/endereço.xs`) possuía apenas campos básicos sem os atributos de endereço completos.

## Objetivo
Atualizar o schema da tabela `USER` e o endpoint `signup_POST.xs` para armazenar `cpf` e `birth_date`, além de enriquecer o schema da tabela de endereços para suportar o gerenciamento completo de múltiplos endereços do usuário no banco de dados.

## Escopo
- Adicionar `cpf` e `birth_date` em `table/user.xs` e `api/autentificacao/auth/signup_POST.xs`.
- Atualizar `table/endereço.xs` com campos de endereço (`user_id`, `title`, `cep`, `street`, `number`, `complement`, `neighborhood`, `city`, `state`, `is_main`).
- Validar a compilação e rastrear em OpenSpec.
