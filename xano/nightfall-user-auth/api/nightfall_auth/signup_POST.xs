query "signup" verb=POST {
  api_group = "NightFall Authentication"
  description = "Create a NightFall account"

  input {
    email email filters=trim|lower
    text password filters=min:8
  }

  stack {
    db.has usuario {
      field_name = "email"
      field_value = $input.email
    } as $email_exists
  
    precondition ($email_exists == false) {
      error_type = "accessdenied"
      error = "Este e-mail já está cadastrado."
    }
  
    db.add usuario {
      enforce_hidden_fields = false
      data = {
        email    : $input.email
        password : $input.password
      }
    } as $account
  }

  response = {
    success: true
    id     : $account.id
    email  : $input.email
  }
  guid = "3uedTS7JaFCBGAWeG65wTQmXIWs"
}
