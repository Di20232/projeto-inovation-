// Update Cliente record
query "cliente/{cliente_id}" verb=PUT {
  api_group = "produtoCRUD"

  input {
    int cliente_id? filters=min:1
    dblink {
      table = "Cliente"
    }
  }

  stack {
    db.edit Cliente {
      field_name = "id"
      field_value = $input.cliente_id
      enforce_hidden_fields = false
      data = {
        Nome               : $input.Nome
        status_do_pedido_id: $input.status_do_pedido_id
        user_id            : $input.user_id
      }
    } as $model
  }

  response = $model
  guid = "4qR0lz1PlBzOJplvCwf6W2N7tR0"
}