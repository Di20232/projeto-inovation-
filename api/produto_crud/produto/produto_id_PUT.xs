// Update produto record
query "produto/{produto_id}" verb=PUT {
  api_group = "produtoCRUD"

  input {
    int produto_id? filters=min:1
    dblink {
      table = "produto"
    }
  }

  stack {
    db.edit produto {
      field_name = "id"
      field_value = $input.produto_id
      enforce_hidden_fields = false
      data = {}
    } as $model
  }

  response = $model
  guid = "xWuQo7uoc8nKsciyNU89aUiJaNk"
}