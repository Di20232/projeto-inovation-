// Get the record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "autentificação"
  auth = "USER"

  input {
  }

  stack {
    db.get USER {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "password", "cliente_id"]
    } as $USER
  }

  response = $USER
  guid = "TKu9IRVAzaUzDcWy-TTDLLfrEMg"
}