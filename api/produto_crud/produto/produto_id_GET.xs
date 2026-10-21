// Get produto record
query "produto/{produto_id}" verb=GET {
  api_group = "produtoCRUD"

  input {
    int produto_id? filters=min:1
  }

  stack {
    db.get produto {
      field_name = "id"
      field_value = $input.produto_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "bocNCW6PsL_9Z1nOO2LCsjz70uw"
}