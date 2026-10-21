// Edit PEPEL record
query "pepel/{pepel_id}" verb=PATCH {
  api_group = "ViaCEP"

  input {
    int pepel_id? filters=min:1
    dblink {
      table = "PEPEL"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch PEPEL {
      field_name = "id"
      field_value = $input.pepel_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $pepel
  }

  response = $pepel
  guid = "Npt2KvdCvV2xHEgWXyOU-GC3PnM"
}