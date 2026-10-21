// Query all cep records
query cep verb=GET {
  api_group = "CEP"

  input {
  }

  stack {
    db.query cep {
      return = {type: "list"}
    } as $cep
  }

  response = $cep
  guid = "q_5pdx43Yh4d6PFyYXTYjd9gjSY"
}