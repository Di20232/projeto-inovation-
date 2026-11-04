# Design: Atualização dos Schemas de Tabelas e Cadastro

## Alterações Propostas
1. **`table/user.xs`**:
   - Adicionar campos `text cpf?` e `text birth_date?`.
2. **`api/autentificacao/auth/signup_POST.xs`**:
   - Adicionar `text cpf?` e `text birth_date?` no `input`.
   - Incluir `cpf: $input.cpf` e `birth_date: $input.birth_date` no objeto de dados passado para `db.add USER`.
3. **`table/endereco.xs`**:
   - Adicionar campos para `user_id`, `title`, `cep`, `street`, `number`, `complement`, `neighborhood`, `city`, `state`, e `boolean is_main`.
