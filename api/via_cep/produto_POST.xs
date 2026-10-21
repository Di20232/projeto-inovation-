// Add produto record
query produto verb=POST {
  api_group = "ViaCEP"

  input {
    dblink {
      table = "produto"
    }
  }

  stack {
    db.add produto {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $produto
  }

  response = $produto
  guid = "OPhh_APun9I2LxMIYZaR2BRcpVw"
}