query upsetCEP verb=POST {
  api_group = "CEP"

  input {
    text CEP? filters=trim
    text UF? filters=trim
    text CIDADE? filters=trim
  }

  stack {
    db.get cep {
      field_name = "id_CEP"
      field_value = $input.CEP
    } as $cep1
  
    conditional {
      if ($var.CEP1[0].cep == $input.CEP) {
        db.patch cep {
          field_name = "id"
          field_value = "$var.CEP1[0].id"
          data = `{'CIDADE':$input.cidade,'UF':$input.estado`
        } as $cep2
      }
    
      else {
        db.add cep {
          enforce_hidden_fields = false
          data = {CEP: $input.CEP, UF: $input.UF, CIDADE: $input.CIDADE}
        } as $cep2
      }
    }
  }

  response = $cep1
  guid = "oOJx75knWvy-Az9_LE6-Bo1zrb8"
}