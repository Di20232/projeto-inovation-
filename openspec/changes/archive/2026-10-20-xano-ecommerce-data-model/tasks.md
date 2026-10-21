## 1. Inspect Xano and existing registration flow

- [x] 1.1 Inspect the authenticated Xano workspace and active branch; verify existing exported table/API documents and confirm whether an isolated development branch is available.
- [x] 1.2 Inspect the current Reflex form and local Xano auth examples; define the registration endpoint and response fields without exposing passwords.

## 2. Implement Xano registration

- [x] 2.1 Add the `usuario` authentication table with normalized unique email and protected password fields; validate its XanoScript.
- [x] 2.2 Add a dedicated public signup API group and endpoint that validates input, handles duplicates, writes through Xano password hashing, and returns only safe account fields; validate its XanoScript.
- [x] 2.3 Connect the `/login` form to the Xano signup endpoint using a Reflex event; verify the configured default URL, validation feedback, service-error handling, success confirmation, and password clearing.

## 3. Review and publish safely

- [x] 3.1 Run focused Python/Reflex compile checks; review the response projection to verify password hashes are never returned.
- [x] 3.2 Run `xano workspace push --dry-run` for the isolated sync directory, present the exact preview, and obtain explicit user approval before publishing.
- [x] 3.3 After explicit approval, push only the reviewed auth table/API documents to the selected Xano branch, pull them back to verify publication, and confirm invalid input is rejected without creating an account.
