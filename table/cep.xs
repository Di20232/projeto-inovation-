table cep {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    enum CEP? {
      values = [""]
    }
  
    text UF? filters=trim
    text CIDADE? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "onOy_lqkltS2tlShobjqzUc-CDw"
}