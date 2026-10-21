// Get produto record
query "produto/{produto_id}" verb=GET {
  api_group = "ViaCEP"

  input {
    int produto_id? filters=min:1
  }

  stack {
    db.get produto {
      field_name = "id"
      field_value = $input.produto_id
    } as $produto
  
    precondition ($produto != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $produto
  guid = "cNt2fGmk2Pm5hhIKZY1BQm8JxAY"
}