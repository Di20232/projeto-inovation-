// Get PEPEL record
query "pepel/{pepel_id}" verb=GET {
  api_group = "ViaCEP"

  input {
    int pepel_id? filters=min:1
  }

  stack {
    db.get PEPEL {
      field_name = "id"
      field_value = $input.pepel_id
    } as $pepel
  
    precondition ($pepel != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $pepel
  guid = "s4K0uT0PdHHJISNvhJG4kBv4Aww"
}