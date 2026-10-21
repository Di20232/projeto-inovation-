## Why

The NightFall login route currently presents email and password fields but does not create an account or persist user data. New visitors need a secure registration flow backed by the selected Xano workspace.

## What Changes

- Add an Xano authentication table named `usuario` with normalized unique email and a protected password field.
- Add a public Xano signup endpoint that validates inputs, creates the account, and never returns the password.
- Connect the current Reflex form to that endpoint using server-side configuration and provide clear validation, success, and service-error feedback.
- Store passwords through Xano's authenticated-table password handling; never persist or log plaintext passwords in application code.

## Capabilities

### New Capabilities
- `xano-user-registration`: Secure account creation through Xano.

### Modified Capabilities
- `login-screen`: Change the current visual-only form into an account-registration form.

## Impact

- XanoScript table and API group/endpoint under `xano/nightfall-user-auth/`.
- The `/login` route in `python/python.py` and a server-side `XANO_SIGNUP_URL` setting.
- The connected Xano workspace's active `v1` branch is currently the only available branch. Changes will be previewed with the CLI dry-run and require explicit approval before publishing to that active branch.
