// Dados do usuário do token, sem a senha. Serve para o backend reconferir is_admin.
// AINDA NÃO PUBLICADO no workspace do Xano (precisa de quem tem acesso a ele).
query "me" verb=GET {
  api_group = "NightFall Authentication"
  description = "Usuário autenticado (id, email, is_admin)"
  auth = "usuario"

  input {
  }

  stack {
    db.get usuario {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "email", "is_admin"]
    } as $user
  }

  response = {id: $user.id, email: $user.email, is_admin: $user.is_admin}
}
