# Tasks: Exibir nome do usuário logado e redirecionar para a home

- [x] 1. Criar proposta, design, spec e tasks no OpenSpec (`openspec/changes/2026-10-22-login-estado-usuario/`).
- [ ] 2. Implementar `AuthState` em `python/python.py` para armazenar `is_logged_in`, `user_name` e a ação de logout.
- [ ] 3. Atualizar `LoginState.login` para definir o `AuthState` e retornar `rx.redirect("/")` no sucesso.
- [ ] 4. Atualizar o componente de cabeçalho na função `index` para exibir o nome do usuário logado ou o botão de login condicionalmente.
- [ ] 5. Executar `reflex compile --dry` para validar a compilação.
