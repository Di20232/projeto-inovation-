// Query all produto records
query produto verb=GET {
  api_group = "ViaCEP"

  input {
  }

  stack {
    db.query produto {
      return = {type: "list"}
    } as $produto
  }

  response = $produto
  guid = "YZMQPt4q_PyLG0dqgD0ohSUhaZE"
}