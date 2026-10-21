// Send an email via Sendgrid using a dynamic template.
function sendgrid_dynamic_send {
  input {
    // The email address to send the email
    email to_email
  
    // The sendgrid template ID
    text template_id
  
    json data?
  }

  stack {
    precondition ($env.workspace.sendgrid_api_key != "") {
      error = 'Please set your "sendgrid_api_key" environment variable.'
    }
  
    precondition ($env.workspace.sendgrid_from_email != "") {
      error = 'Please set your "sendgrid_from_email" environment variable.'
    }
  
    // Makes an API request to SendGrid to send an email through a template
    api.request {
      url = "https://api.sendgrid.com/v3/mail/send"
      method = "POST"
      params = {}
        |set:"from":({}
          |set:"email":$env.workspace.sendgrid_from_email
        )
        |set:"personalizations":([]
          |push:({}
            |set:"to":([]
              |push:({}|set:"email":$input.to_email)
            )
            |set:"dynamic_template_data":$input.data
          )
        )
        |set:"template_id":$input.template_id
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
  guid = "aEgqC7dMIlrSZwcBXh-j7bpFfAI."
}