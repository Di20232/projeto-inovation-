# Design

- `admin_page` usa `rx.cond(AuthState.is_admin, admin_panel(), admin_restricted())`.
- O bloqueio é de tela. A segurança das alterações continua nas checagens `_is_admin` dos eventos.
- Conteúdo fixo da interface é compilado no frontend; escondê-lo não o protege.
