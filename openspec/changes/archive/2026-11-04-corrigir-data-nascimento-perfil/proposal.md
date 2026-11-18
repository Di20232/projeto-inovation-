# Proposta: Correção da Exibição da Data de Nascimento no Perfil

## Contexto
Embora o CPF agora seja propagado corretamente do cadastro para o perfil, a Data de Nascimento ainda pode não refletir o valor inserido ou formatado corretamente na tela de Meus Dados (`/perfil`).

## Objetivo
Garantir que a Data de Nascimento informada no cadastro seja formatada corretamente (`DD/MM/YYYY`) e propagada integralmente para o `AuthState.user_birth_date`.

## Escopo
- Assegurar o uso de `format_birth_date(birth_date)` ao atribuir a data de nascimento no `AuthState` durante o registro (`RegistrationState.register`).
- Validar e registrar a change em OpenSpec.
- Verificar compilação.
