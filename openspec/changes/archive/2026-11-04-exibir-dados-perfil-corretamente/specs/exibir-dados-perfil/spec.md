# Especificação: Exibição de CPF e Data de Nascimento no Perfil

## Requisitos
1. **Cadastro Bem-Sucedido**: Quando o usuário realiza o cadastro com sucesso em `/cadastro`, os dados (`name`, `email`, `cpf`, `birth_date`) devem ser salvos no `AuthState` e o usuário deve ser marcado como logado (`is_logged_in = True`).
2. **Visualização no Perfil**: Na tela de perfil (`/perfil`), a aba "Meus Dados" deve exibir corretamente o CPF formatado e a Data de Nascimento informados no cadastro.
3. **Login**: Ao efetuar login, se o usuário possuir CPF e Data de Nascimento salvos ou definidos, estes devem ser preservados e exibidos corretamente.
