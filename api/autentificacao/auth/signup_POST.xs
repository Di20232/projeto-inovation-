// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "autentificação"

  input {
    text name?
    text email?
    text password?
  }

  stack {
    db.get USER {
      field_name = "email"
      field_value = $input.email
    } as $USER
  
    precondition ($USER == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add USER {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
      }
    } as $USER
  
    security.create_auth_token {
      table = "USER"
      extras = {}
      expiration = 86400
      id = $USER.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "9FFqJwHOvNmynalkhpagTtbYm9s"
}