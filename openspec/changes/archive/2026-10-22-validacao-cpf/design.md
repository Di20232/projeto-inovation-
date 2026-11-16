# Design: Validação de CPF no Cadastro NightFall

## Arquitetura
- **Estado**: `RegistrationState.register` passará a validar o CPF informado.
- **Validação**: Limpeza de caracteres não numéricos e verificação de tamanho/formato (ou algoritmo de CPF), definindo `registration_message` caso inválido.

## Verificação
- Testar com CPFs válidos e inválidos.
- Documentar requisitos em `specs/validacao-cpf/spec.md`.
