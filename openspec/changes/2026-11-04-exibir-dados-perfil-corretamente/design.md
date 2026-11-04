# Design: Exibição Correta de CPF e Data de Nascimento no Perfil

## Abordagem Técnica
1. **Propagação no Cadastro (`RegistrationState.register`)**:
   - Ao receber `signup_result` com sucesso, obter o estado de `AuthState` e atualizar:
     - `auth_state.user_name = name`
     - `auth_state.user_email = email`
     - `auth_state.user_cpf = format_cpf(cpf)`
     - `auth_state.user_birth_date = format_birth_date(birth_date)`
     - `auth_state.is_logged_in = True`
2. **Propagação no Login (`LoginState.login`)**:
   - Manter dados preenchidos ou permitir sincronização com o perfil.
3. **Persistência / Estado Global (`AuthState`)**:
   - Assegurar que `user_cpf` e `user_birth_date` reflitam os valores reais do usuário logado.
