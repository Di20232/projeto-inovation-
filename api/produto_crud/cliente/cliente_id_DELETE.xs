// Delete Cliente record
query "cliente/{cliente_id}" verb=DELETE {
  api_group = "produtoCRUD"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.del Cliente {
      field_name = "id"
      field_value = $input.cliente_id
    }
  }

  response = null
  guid = "_Q2roTAcG8JZqBbYqJP2YLvcReE"
}