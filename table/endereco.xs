table "endereço" {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }

    int user_id? {
      table = "USER"
    }

    text title? filters=trim
    text cep? filters=trim
    text street? filters=trim
    text number? filters=trim
    text complement? filters=trim
    text neighborhood? filters=trim
    text city? filters=trim
    text state? filters=trim
    boolean is_main?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "7rqmaRSqEfJxMnz6bW9lBECxLmY"
}
