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
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
  guid = "_NtFv8WIb5EkuXgC5e4YuaI9GVU"
}
