// Query all Cliente records
query cliente verb=GET {
  api_group = "produtoCRUD"

  input {
  }

  stack {
    db.query Cliente {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "BASdDBQB5lPFp7HebhBq0DAc8yk"
}