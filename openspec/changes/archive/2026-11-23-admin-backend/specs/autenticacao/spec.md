# Spec: Autenticação e administrador

## Requisitos
- Nenhuma credencial de administrador fica no código-fonte.
- É administrador quem: (a) bate com `ADMIN_EMAIL` + `ADMIN_PASSWORD_HASH` do .env; ou (b) faz login no Xano e recebe `user.is_admin = true`.
- Sem as variáveis do .env e sem Xano, ninguém é administrador.
- Com `XANO_LOGIN_URL` configurada, senha errada é recusada e falha do Xano impede o login (sem cair no modo local).
- Conta criada pelo cadastro nunca é administradora; o logout limpa o privilégio e o token.
