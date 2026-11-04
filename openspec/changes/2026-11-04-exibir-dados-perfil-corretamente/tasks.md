# Tarefas: Exibição Correta de CPF e Data de Nascimento no Perfil

- [x] Atualizar `RegistrationState.register` em `python/python.py` para popular `AuthState` (`user_name`, `user_email`, `user_cpf`, `user_birth_date`, `is_logged_in`) após sucesso no cadastro.
- [x] Atualizar `LoginState.login` para garantir que `user_cpf` e `user_birth_date` sejam mantidos ou preenchidos.
- [x] Adicionar botão "Salvar Alterações" na aba Meus Dados do perfil chamando `AuthState.save_profile`.
- [x] Validar a compilação com `reflex compile --dry` (Sucesso em 1.57s).
