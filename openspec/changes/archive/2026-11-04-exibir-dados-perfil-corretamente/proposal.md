# Proposta: Exibição Correta de CPF e Data de Nascimento no Perfil do Usuário

## Contexto
Atualmente, na tela de Meus Dados do Perfil (`/perfil`), os campos de CPF e Data de Nascimento do usuário podem vir em branco ou com valores genéricos/placeholders, pois o fluxo de cadastro e login não transfere corretamente esses dados inseridos pelo usuário para o `AuthState`.

## Objetivo
Garantir que os dados preenchidos pelo usuário no cadastro (`RegistrationState`) ou recuperados no login sejam propagados corretamente para o `AuthState` e exibidos na página de perfil (`/perfil`).

## Escopo
- Propagar `cpf` e `birth_date` do `RegistrationState` para o `AuthState` ao concluir o cadastro com sucesso.
- Garantir que o `AuthState` inicialize ou receba o CPF e a Data de Nascimento reais do usuário ao fazer login.
- Atualizar a UI do perfil em `python/python.py` para exibir e permitir edição/salvamento desses campos.
