// Delete produto record
query "produto/{produto_id}" verb=DELETE {
  api_group = "produtoCRUD"

  input {
    int produto_id? filters=min:1
  }

  stack {
    db.del produto {
      field_name = "id"
      field_value = $input.produto_id
    }
  }

  response = null
  guid = "p27dO41iZa1Xcu4SOqOhq3LLI6c"
}