// Login and retrieve an authentication token
query "auth/login" verb=POST {
  api_group = "autentificação"

  input {
    text email? filters=trim
    text password?
  }

  stack {
    db.get USER {
      field_name = "email"
      field_value = $input.email
      output = ["id", "created_at", "name", "email", "password"]
    } as $USER
  
    precondition ($USER != null) {
      error = "Invalid Credentials."
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $USER.password
    } as $pass_result
  
    precondition ($pass_result) {
      error = "Invalid Credentials."
    }
  
    security.create_auth_token {
      table = "USER"
      extras = {}
      expiration = 86400
      id = $USER.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "-8rrRCEp1T0_y3ITqAD36drxnW0"
}