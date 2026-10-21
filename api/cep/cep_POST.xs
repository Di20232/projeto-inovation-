// Add cep record
query cep verb=POST {
  api_group = "CEP"

  input {
    dblink {
      table = "cep"
    }
  }

  stack {
    db.add cep {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $cep
  }

  response = $cep
  guid = "s6OXnErn9o0oNFVpjJ0cl22k8aY"
}