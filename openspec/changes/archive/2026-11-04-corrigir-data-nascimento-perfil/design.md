# Design: Correção da Data de Nascimento no Perfil

## Abordagem Técnica
Em `RegistrationState.register`, atualizar a atribuição para:
```python
auth_state.user_birth_date = format_birth_date(birth_date)
```
Garantindo a formatação consistente (`DD/MM/YYYY`) no perfil do usuário.
