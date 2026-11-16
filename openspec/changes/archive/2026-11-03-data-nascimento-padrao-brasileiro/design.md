# Design: Data de Nascimento no Padrão Brasileiro

## Arquitetura
- **Utilitário**: Função `format_birth_date(value: str) -> str` que filtra dígitos e formata como `DD/MM/YYYY`.
- **Estados**:
  - `RegistrationState.set_birth_date`: aplica `format_birth_date`.
  - `AuthState.set_user_birth_date`: aplica `format_birth_date`.
- **Interface**:
  - `rx.input` com `placeholder="DD/MM/YYYY"`, `max_length="10"`, e sem `type="date"` em `/cadastro` e `/perfil`.

## Verificação
- Testar digitação no campo de data de nascimento nas telas de cadastro e perfil.
- Validar formatação automática `DD/MM/YYYY`.
