# Proposta: Verificação e Validação de CPF no Cadastro

## Contexto
O formulário de cadastro coleta o CPF do usuário, mas atualmente realiza apenas a verificação de campo preenchido, sem validar o formato ou a integridade dos dígitos.

## Objetivo
Garantir que o CPF informado no cadastro seja validado (formato e/ou algoritmo de dígitos verificadores), impedindo o envio de CPFs inválidos e fornecendo feedback claro em português.

## Escopo
- Validação do CPF no `RegistrationState` antes de enviar os dados ao Xano.
- Documentação da especificação em OpenSpec.
