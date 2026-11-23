// Login do NightFall: confere a senha (hash do campo password) e devolve o token
// e se o usuário é administrador. O app (admin_auth.xano_login) usa user.is_admin.
// AINDA NÃO PUBLICADO no workspace do Xano (precisa de quem tem acesso a ele).
query "login" verb=POST {
  api_group = "NightFall Authentication"
  description = "Login de conta NightFall com retorno de is_admin"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get usuario {
      field_name = "email"
      field_value = $input.email
      output = ["id", "email", "password", "is_admin"]
    } as $user

    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Credenciais inválidas."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_ok

    precondition ($pass_ok) {
      error_type = "accessdenied"
      error = "Credenciais inválidas."
    }

    security.create_auth_token {
      table = "usuario"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {
    authToken: $authToken
    user     : {id: $user.id, email: $user.email, is_admin: $user.is_admin}
  }
}
