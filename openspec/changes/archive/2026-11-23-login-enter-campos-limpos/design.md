# Design

- `LoginState.submit_on_enter(key)`: se a tecla for `Enter`, devolve o evento `LoginState.login`. Ligado no `on_key_down` dos dois campos.
- `LoginState.reset_form()`: zera `email`, `password`, `login_message` e `login_succeeded`. Vira o `on_load` da página `/login`.
- O botão continua `type="button"` com `on_click=LoginState.login`.
