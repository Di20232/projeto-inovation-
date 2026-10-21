// Edit Cliente record
query "cliente/{cliente_id}" verb=PATCH {
  api_group = "produtoCRUD"

  input {
    int cliente_id? filters=min:1
    dblink {
      table = "Cliente"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch Cliente {
      field_name = "id"
      field_value = $input.cliente_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "OlAieBDcZF5EzrMe9pT281Xe2yA"
}