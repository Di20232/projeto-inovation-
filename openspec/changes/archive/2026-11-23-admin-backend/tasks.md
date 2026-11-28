# Tarefas

- [x] 1. Criar `admin_auth.py` (hash PBKDF2, admin do .env, cliente de login do Xano).
- [x] 2. Criar `scripts/gerar_hash_admin.py`.
- [x] 3. Trocar a credencial fixa do `LoginState.login` pela checagem no servidor; cadastro sem admin; logout limpa o token.
- [x] 4. Escrever `is_admin` na tabela `usuario` e os endpoints `login` e `me` do grupo `nightfall-auth`.
- [x] 5. Atualizar `.env.example`.
- [x] 6. Testes `tests_admin_auth.py` (9) + `tests_unitarios.py` (10) e `reflex compile --dry`.
- [x] 7. Teste no navegador com Xano simulado: admin do .env e admin do Xano veem "Gerenciar Site"; cliente do Xano não; senha errada é recusada.
- [ ] 8. Publicar `usuario.xs`, `login_POST.xs` e `me_GET.xs` no workspace do Xano, marcar o admin real com `is_admin = true` e configurar `XANO_LOGIN_URL`.
