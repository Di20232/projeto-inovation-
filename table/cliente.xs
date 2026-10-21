table Cliente {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text Nome? filters=trim
    int status_do_pedido_id? {
      table = "Status do pedido"
    }
  
    int user_id? {
      table = "USER"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "ChjXaiL_pfjPJBZvGFqyp1yj7A8"
}