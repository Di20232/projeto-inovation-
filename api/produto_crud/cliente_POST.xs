// Add Cliente record
query cliente verb=POST {
  api_group = "produtoCRUD"

  input {
    dblink {
      table = "Cliente"
    }
  }

  stack {
    db.add Cliente {
      enforce_hidden_fields = false
      data = {
        created_at         : "now"
        Nome               : $input.Nome
        status_do_pedido_id: $input.status_do_pedido_id
        user_id            : $input.user_id
      }
    } as $model
  }

  response = $model
  guid = "m9XIRwt9q4rs7teonQH52H05S80"
}