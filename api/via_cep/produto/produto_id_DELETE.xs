// Delete produto record.
query "produto/{produto_id}" verb=DELETE {
  api_group = "ViaCEP"

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
  guid = "qWvE-MdTgDzHftDsvJhH_hlEZlY"
}