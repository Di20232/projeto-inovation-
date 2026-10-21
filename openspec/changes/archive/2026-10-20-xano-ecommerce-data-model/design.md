## Context

The `/login` route currently renders email and password fields without submitting them. The authenticated Xano workspace is `151378`; its live `v1` branch contains no exported database or API documents, and the account does not permit creation of a development branch. The repository's existing `USER` and signup exports have GUIDs and therefore are not assumed to exist in this live workspace.

## Goals / Non-Goals

**Goals:**
- Create a new Xano auth table named `usuario` and a signup endpoint with an explicit, safe response.
- Send registration requests from a Reflex server event to a server-configured Xano endpoint.
- Validate the implementation and preview remote changes without modifying the active branch until the user approves the CLI preview.

**Non-Goals:**
- Build login/authenticated-session behavior, password reset, profile management, or an admin role.
- Create or alter unrelated tables or endpoints.
- Store plaintext passwords, expose Xano management credentials, or publish to the active branch without explicit approval.

## Decisions

### Use a Xano authentication table

Create `usuario` with `auth = true`, an auto-generated integer ID, private creation timestamp, normalized email with a unique index, and an internal/sensitive Xano password field. Xano's authentication-table password handling stores the password hash; the API response selects only a safe account identifier and email. A unique database index is the final protection against duplicate registrations arriving concurrently.

### Implement registration as a dedicated public API operation

Create a project-specific API group and a `POST /signup` endpoint. Validate email and an 8-character minimum password, reject duplicate email addresses, and return only a safe success payload. Do not mint an auth token because the requested feature is registration, not sign-in. The Reflex application uses the endpoint's complete URL from `XANO_SIGNUP_URL`; this avoids embedding a presumed API group URL in code.

### Submit through the Reflex server

Use an asynchronous server-side event to call Xano. Keep credentials out of browser-delivered configuration and clear the password from State after each request. Show an explicit success, duplicate/validation error, missing-configuration error, or connection error. Map backend failures to safe user-facing messages instead of exposing raw response bodies.

### Gate publishing to the live branch

The only available Xano branch is the active `v1`, and creating a development branch was rejected by Xano's plan restrictions. Keep a sync-aware local copy of the current workspace, run XanoScript validation and `workspace push --dry-run`, and show that preview to the user. Do not run the actual push until the user explicitly approves the preview.

## Risks / Trade-offs

- [The Xano workspace is production-only] → Limit the preview to the new auth table and signup API and require explicit user approval before publishing.
- [Email uniqueness races] → Enforce a unique Xano email index in addition to the endpoint's duplicate lookup.
- [Xano API URL is missing or points to the wrong endpoint] → Require `XANO_SIGNUP_URL`, fail closed, and document the expected endpoint URL without committing credentials.
- [Registration failures leak sensitive details] → Map status codes to controlled messages and never render response bodies or passwords.
