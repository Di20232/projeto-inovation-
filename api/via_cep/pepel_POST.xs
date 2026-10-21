// Add PEPEL record
query pepel verb=POST {
  api_group = "ViaCEP"

  input {
    dblink {
      table = "PEPEL"
    }
  }

  stack {
    db.add PEPEL {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $pepel
  }

  response = $pepel
  guid = "g3zmCGzb_35iFH5IifXJneBNATs"
}