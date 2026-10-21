// Query all produto records
query produto verb=GET {
  api_group = "produtoCRUD"

  input {
  }

  stack {
    db.query produto {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "PihdddyzlAOsuBA7_wcd5tIcvA4"
}