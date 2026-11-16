// Get Cliente record
query "cliente/{cliente_id}" verb=GET {
  api_group = "produtoCRUD"
  auth = "USER"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.get Cliente {
      field_name = "id"
      field_value = $input.cliente_id
    } as $model

    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }

    precondition ($model.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Unauthorized access to customer record."
    }
  }

  response = $model
  guid = "WuhlfQFa2CwUXHjNWRxV1mdtenQ"
}
