// Get Cliente record
query "cliente/{cliente_id}" verb=GET {
  api_group = "produtoCRUD"

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
  }

  response = $model
  guid = "WuhlfQFa2CwUXHjNWRxV1mdtenQ"
}