// Delete PEPEL record.
query "pepel/{pepel_id}" verb=DELETE {
  api_group = "ViaCEP"

  input {
    int pepel_id? filters=min:1
  }

  stack {
    db.del PEPEL {
      field_name = "id"
      field_value = $input.pepel_id
    }
  }

  response = null
  guid = "NuykZvGWBf29nGhPK1iLEfXPI9U"
}