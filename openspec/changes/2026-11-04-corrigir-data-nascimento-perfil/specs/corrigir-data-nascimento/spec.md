# Especificação: Correção da Data de Nascimento no Perfil

## Requisitos
1. **Propagação Formatada**: A data de nascimento informada durante o cadastro deve ser formatada com `format_birth_date()` e armazenada em `AuthState.user_birth_date`.
2. **Exibição na Aba Meus Dados**: O campo de Data de Nascimento em `/perfil` deve refletir corretamente o valor cadastrado pelo usuário.
