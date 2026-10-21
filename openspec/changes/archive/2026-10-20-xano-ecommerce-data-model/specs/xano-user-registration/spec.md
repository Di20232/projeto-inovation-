## Purpose

Allow a visitor to create a NightFall account through a secure registration endpoint backed by the Xano authentication table.

## ADDED Requirements

### Requirement: Secure Xano user table
The system SHALL persist registered accounts in an authentication-enabled Xano table named `usuario`. Each account SHALL have a normalized unique email address and a password handled and stored as a Xano password hash. The password SHALL NOT be returned by any registration response or stored in plaintext by the application.

#### Scenario: Account is stored
- **WHEN** a valid registration is submitted with an email address and password of at least 8 characters
- **THEN** Xano creates one account with a normalized email and a password hash

#### Scenario: Email already exists
- **WHEN** a registration is submitted with an email address already associated with an account
- **THEN** the endpoint rejects the duplicate without creating another account

#### Scenario: Registration response is returned
- **WHEN** Xano successfully creates an account
- **THEN** the response contains a safe success result and does not include the password or password hash

### Requirement: Public registration endpoint validation
The system SHALL provide a public registration endpoint that requires a syntactically valid email address and a non-empty password of at least 8 characters. Invalid input and duplicate-email attempts SHALL return an explicit error and SHALL NOT create an account.

#### Scenario: Visitor submits valid registration details
- **WHEN** the visitor submits a valid email address and qualifying password
- **THEN** the endpoint creates the account and returns success

#### Scenario: Visitor submits invalid registration details
- **WHEN** the visitor submits a malformed email address or a password shorter than 8 characters
- **THEN** the endpoint rejects the request and creates no account

### Requirement: Login-route registration feedback
The `/login` route SHALL present the email and password form as account registration. The form SHALL submit the credentials to the server-configured Xano signup endpoint, display explicit success or failure feedback, and clear the password from application state after the request. Missing endpoint configuration or an unavailable Xano service SHALL be reported as an error rather than a successful registration.

#### Scenario: Registration succeeds
- **WHEN** Xano accepts the registration
- **THEN** the page confirms that the account was created and clears the password field

#### Scenario: Registration fails
- **WHEN** Xano rejects the registration or cannot be reached
- **THEN** the page displays a useful failure message and does not claim that an account was created

#### Scenario: Signup endpoint is not configured
- **WHEN** a visitor submits the form without a configured Xano signup URL
- **THEN** the page displays a configuration error and does not send the credentials anywhere
