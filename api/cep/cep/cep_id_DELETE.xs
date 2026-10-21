// Delete cep record.
query "cep/{cep_id}" verb=DELETE {
  api_group = "CEP"

  input {
    int cep_id? filters=min:1
  }

  stack {
    db.del cep {
      field_name = "id"
      field_value = $input.cep_id
    }
  }

  response = null
  guid = "K-u8ZMeIdTNeTTAx2w3K-vlLmBU"
}