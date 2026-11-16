# Especificação: Limpeza de Campos do Formulário de Cadastro

## Requisitos
1. **Redefinição Pós-Cadastro**: Quando um usuário cria uma conta com sucesso na tela `/cadastro`, os campos `name`, `cpf`, `birth_date`, `email` e `password` do `RegistrationState` devem ser limpos (`""`).
2. **Prevenção de Persistência Indevida**: Dados do usuário anterior não devem persistir no formulário de cadastro para o próximo acesso à tela.
