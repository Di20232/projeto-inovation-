# Design

## Módulo `admin_auth.py`
- `hash_admin_password` / `verify_admin_password`: formato `pbkdf2_sha256:<iterações>:<salt>:<hash>` (sem `$`, por causa do .env); comparação com `hmac.compare_digest`.
- `check_env_admin(email, senha)`: só é admin se as duas variáveis existirem e baterem. Com e-mail diferente, ainda calcula o hash (não revela pelo tempo).
- `xano_login(email, senha)`: `None` se `XANO_LOGIN_URL` vazia; 200 com `authToken` → `ok` e `is_admin` (só `true` literal); 400/401/403 → credenciais inválidas; rede, 404, 5xx, JSON inválido ou sem token → `XanoUnavailable`.

## Login (`LoginState.login`)
1. Admin do .env (em thread, para não travar o servidor).
2. Senão, Xano se configurado (decide login e `is_admin`; indisponível → mensagem, sem login).
3. Senão, login local de desenvolvimento **sem** privilégio de admin.
- Token do Xano em `AuthState._auth_token` (variável só do backend, não vai ao navegador).

## Xano (`xano/nightfall-user-auth/`)
- `table/usuario.xs`: `bool is_admin?=false` (internal).
- `api/nightfall_auth/login_POST.xs` e `me_GET.xs`.

## Configuração
- `.env.example` documenta `XANO_LOGIN_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD_HASH` e `NIGHTFALL_SIMULATED_PAYMENTS`.
