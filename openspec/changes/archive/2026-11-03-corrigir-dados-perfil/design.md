# Design: Correção de Dados no Perfil

## Arquitetura
- **Estado (`AuthState`)**:
  - `user_cpf`: inicializado com valor padrão ou preenchido no login.
  - `user_birth_date`: inicializado com valor padrão ou preenchido no login.
  - Novos eventos: `set_user_name(self, name: str)` e `save_profile(self)`.
- **Interface**:
  - Aba "Meus Dados" em `/perfil` com inputs para Nome, CPF, Data de Nascimento, E-mail e botão "Salvar Alterações".

## Verificação
- Testar login e verificação de CPF e Data de Nascimento na página de perfil.
