# Proposta: Limpeza de Campos do Formulário de Cadastro após Sucesso

## Contexto
Atualmente, quando o usuário conclui o cadastro de conta com sucesso em `/cadastro`, os campos do formulário (nome, CPF, data de nascimento e e-mail) continuam preenchidos com os dados da última tentativa ou usuário cadastrado.

## Objetivo
Limpar automaticamente todos os campos do `RegistrationState` (`name`, `cpf`, `birth_date`, `email`, `password`) quando o cadastro for concluído com sucesso, garantindo privacidade e formulário limpo para novos cadastros.

## Escopo
- Atualizar o método `register` em `RegistrationState` para redefinir os campos para vazio (`""`) em caso de sucesso no cadastro.
- Criar a especificação e rastreabilidade em OpenSpec.
- Validar a compilação.
