// Send a plain text email via SendGrid
function sendgrid_basic_send {
  input {
    // The email address to send the email
    email to_email
  
    // The subject of the email
    text subject
  
    // The body of the email
    text body
  }

  stack {
    precondition ($env.workspace.sendgrid_api_key != "") {
      error = 'Please set your "sendgrid_api_key" environment variable.'
    }
  
    precondition ($env.workspace.sendgrid_from_email != "") {
      error = 'Please set your "sendgrid_from_email" environment variable.'
    }
  
    // Makes an API request to SendGrid to send an email
    api.request {
      url = "https://api.sendgrid.com/v3/mail/send"
      method = "POST"
      params = {}
        |set:"subject":$input.subject
        |set:"from":({}
          |set:"email":$env.workspace.sendgrid_from_email
        )
        |set:"content":([]
          |push:({}
            |set:"type":"text/plain"
            |set:"value":$input.body
          )
        )
        |set:"personalizations":([]
          |push:({}
            |set:"to":([]
              |push:({}|set:"email":$input.to_email)
            )
          )
        )
      headers = []
        |push:"Content-Type: application/json"
        |push:("Authorization: Bearer %s"
          |sprintf:$env.workspace.sendgrid_api_key
        )
    } as $api_result
  
    precondition ($api_result.response.status == 202) {
      error = $api_result.response.result.errors.0.message
    }
  }

  response = null
  guid = "c7O6M5u96POavtOn1PLiTwxu5dw."
}