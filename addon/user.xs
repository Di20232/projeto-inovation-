addon user {
  input {
    int user_id? {
      table = ""
    }
  }

  stack {
    db.query "" {
      where = $db.user.id == $input.user_id
      return = {type: "single"}
    }
  }

  guid = "fI5VpxYryCJpzhx40j0gOMcUebI"
}