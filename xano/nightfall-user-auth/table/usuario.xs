table "usuario" {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }

    email email filters=trim|lower {
      sensitive = true
      visibility = "internal"
    }
  
    password password {
      sensitive = true
      visibility = "internal"
    }

    // Privilégio de administrador. Só é alterado direto no Xano (nunca pelo signup).
    bool is_admin?=false {
      visibility = "internal"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
  guid = "_NtFv8WIb5EkuXgC5e4YuaI9GVU"
}
