# Proposta: Checagem de Administrador no Backend

## Contexto
O administrador era definido por e-mail e senha fixos no código (`admin@admin.com` / `admin123`), e o login aceitava qualquer e-mail com senha de 6+ caracteres sem consultar ninguém. O grupo `nightfall-auth` do Xano só tinha cadastro (sem login e sem papel de admin).

## Objetivo
Tirar a credencial do código e decidir quem é admin no servidor, a partir de fontes de verdade fora do código-fonte.

## Escopo
- **Admin local (.env)**: `ADMIN_EMAIL` + `ADMIN_PASSWORD_HASH` (PBKDF2-SHA256, 600 mil iterações), verificados no servidor Reflex. Script `scripts/gerar_hash_admin.py` para gerar o hash sem mostrar a senha.
- **Xano**: campo `is_admin` na tabela `usuario`, endpoints `login` (devolve `authToken` e `user.is_admin`) e `me` no grupo `nightfall-auth`. O app usa o Xano quando `XANO_LOGIN_URL` estiver configurada.
- Cadastro nunca herda admin; logout limpa o token.

## Fora do escopo
- Publicar os `.xs` no workspace do Xano (precisa de quem tem acesso a ele).
- Trocar o login local de desenvolvimento (sem Xano) por login real.
