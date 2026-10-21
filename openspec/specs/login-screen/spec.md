# Login Screen Specification

## Purpose

Oferecer um destino visual para o botão de login da NightFall sem introduzir autenticação, processamento de credenciais ou dependência de dados de usuário.

## Requirements

### Requirement: Navegação para a tela de login
A página inicial SHALL permitir que o visitante abra a tela de login da NightFall pelo botão “Login”, na rota `/login`. A tela de login SHALL oferecer um controle que retorne à página inicial.

#### Scenario: Visitante abre a tela de login
- **WHEN** o visitante ativa o botão “Login” na página inicial
- **THEN** a aplicação navega para `/login` e exibe a tela de login

#### Scenario: Visitante retorna à página inicial
- **WHEN** o visitante ativa o controle de retorno na tela de login
- **THEN** a aplicação navega de volta para a página inicial

### Requirement: Apresentação visual do formulário de login
A rota `/login` SHALL exibir a identidade NightFall em tema escuro com roxo como cor de destaque, campos identificados para e-mail e senha, e um botão “Criar conta”. O conteúdo SHALL informar que o visitante está criando uma conta e permanecer legível e utilizável em telas estreitas e amplas, sem rolagem horizontal da página.

#### Scenario: Visitante visualiza a tela de login
- **WHEN** o visitante abre a rota `/login`
- **THEN** a tela apresenta a marca NightFall, os campos de e-mail e senha e o botão “Criar conta” em uma interface legível

#### Scenario: Visitante acessa a tela em dispositivo estreito
- **WHEN** a tela de cadastro é exibida em uma tela estreita
- **THEN** os campos, rótulos e controles permanecem visíveis e utilizáveis sem rolagem horizontal

### Requirement: Formulário sem autenticação ou persistência
A rota `/login` SHALL atuar como formulário de cadastro e enviar e-mail e senha ao endpoint configurado do Xano somente após o visitante acionar “Criar conta”. O sistema SHALL exibir uma confirmação somente após sucesso informado pelo Xano e SHALL NOT manter a senha no estado da aplicação após o processamento da requisição.

#### Scenario: Visitante ativa o botão do formulário
- **WHEN** o visitante envia um e-mail válido e uma senha com pelo menos 8 caracteres e o Xano confirma a criação
- **THEN** a tela informa que a conta foi criada e limpa o campo de senha

#### Scenario: Cadastro rejeitado ou serviço indisponível
- **WHEN** o Xano rejeita os dados ou não pode ser alcançado
- **THEN** a tela exibe uma mensagem de erro e não informa que a conta foi criada

#### Scenario: Endpoint de cadastro não configurado
- **WHEN** o visitante envia o formulário sem uma URL de cadastro configurada
- **THEN** a tela informa que o cadastro está indisponível e não envia os dados
