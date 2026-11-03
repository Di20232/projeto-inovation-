# Proposta: Correção da Exibição de CPF e Data de Nascimento no Perfil

## Contexto
Na página de perfil (`/perfil` -> Meus Dados), os campos de CPF e Data de Nascimento não apareciam preenchidos porque o login inicial não populava esses dados no estado e faltava um fluxo claro de salvamento de perfil.

## Objetivo
Garantir que o CPF e a Data de Nascimento do usuário sejam preenchidos ao realizar login e possam ser visualizados e atualizados corretamente na aba Meus Dados do perfil.

## Escopo
- Adicionar valores padrão/preenchimento para CPF e Data de Nascimento no `AuthState` e no evento de login.
- Adicionar evento `set_user_name` e `save_profile` no `AuthState`.
- Adicionar botão "Salvar Alterações" na aba Meus Dados.
- Documentar a especificação em OpenSpec.
