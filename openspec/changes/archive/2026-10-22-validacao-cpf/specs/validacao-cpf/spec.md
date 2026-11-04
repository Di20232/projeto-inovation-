## Purpose

Garantir que o CPF informado no cadastro do NightFall seja devidamente verificado e validado.

## ADDED Requirements

### Requirement: Validação de CPF no formulário de cadastro
O sistema SHALL validar o CPF informado pelo usuário no cadastro, exigindo formato correto e/ou dígitos válidos antes de prosseguir com a requisição ao Xano.

#### Scenario: Usuário informa CPF inválido
- **WHEN** o usuário preenche o campo CPF com um número inválido ou incompleto
- **THEN** o sistema exibe mensagem de erro informando que o CPF é inválido e bloqueia o envio

#### Scenario: Usuário informa CPF válido
- **WHEN** o usuário preenche o CPF corretamente
- **THEN** o cadastro prossegue normalmente para a validação dos demais campos e envio ao Xano
