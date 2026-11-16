# Design: Limpeza de Campos do Formulário de Cadastro

## Abordagem Técnica
No bloco `else` de sucesso em `RegistrationState.register`:
```python
            if isinstance(signup_result, dict) and signup_result.get("success") is True:
                self.registration_message = (
                    "Conta criada com sucesso. Bem-vindo ao NightFall!"
                )
                self.registration_succeeded = True

                auth_state = await self.get_state(AuthState)
                auth_state.is_logged_in = True
                auth_state.user_name = name
                auth_state.user_email = email
                auth_state.user_cpf = format_cpf(cpf)
                auth_state.user_birth_date = birth_date

                # Limpa os campos do formulário de cadastro
                self.name = ""
                self.cpf = ""
                self.birth_date = ""
                self.email = ""
                self.password = ""
```
Isso garante que após o sucesso, o formulário fique totalmente limpo.
