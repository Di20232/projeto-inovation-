// Add produto record
query produto verb=POST {
  api_group = "produtoCRUD"

  input {
    dblink {
      table = "produto"
    }
  }

  stack {
    db.add produto {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $model
  }

  response = $model
  guid = "LWNRRb1aXYvmGzWDzJxkOFgk6Tc"
}