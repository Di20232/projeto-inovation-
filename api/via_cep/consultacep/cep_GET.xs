query "consultacep/{cep}" verb=GET {
  api_group = "ViaCEP"

  input {
    text cep? filters=trim
  }

  stack {
    var $url {
      value = "https://viacep.com.br/ws/" ~ $input.cep ~ "/json"
    }
  
    api.request {
      url = $url
      method = "GET"
      params = ""
      headers = ["Content-Type: application/json"]
    } as $api1
  
    var $x1 {
      value = {
        status  : $api1.response.status
        endereco: $api1.response.result
      }
    }
  
    var $erro {
      value = true
    }
  
    // Tenta-se atribuir à variável erro o conteúdo de x1.endereco.erro.
    // 
    // Quando o campo "erro" não existir (consulta deu certo), a tentativa de fazer erro = x1.endereco.erro falha. O Catch captura esta situação e faz com que erro = false (pois a consulta deu certo).
    // 
    try_catch {
      try {
        var $erro {
          value = $x1.endereco.erro
        }
      }
    
      catch {
        var $erro {
          value = false
        }
      }
    }
  
    conditional {
      if ($x1.status == 400 || $erro) {
        var $resp {
          value = {status: false, endereco: null}
        }
      }
    
      else {
        var $resp {
          value = {status: true, endereco: $x1.endereco}
        }
      }
    }
  }

  response = $resp
  guid = "5LTQlC4wIJ6T6SrlNTKoG1UFVCo"
}