// Query all PEPEL records
query pepel verb=GET {
  api_group = "ViaCEP"

  input {
  }

  stack {
    db.query PEPEL {
      return = {type: "list"}
    } as $pepel
  }

  response = $pepel
  guid = "3ma4sUhxjB2uzt57H7tSu5-ak8k"
}