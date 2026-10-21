## Purpose

Oferecer um destino visual para o botão de login da NightFall sem introduzir autenticação, processamento de credenciais ou dependência de dados de usuário.

## ADDED Requirements

### Requirement: Navegação para a tela de login
A página inicial SHALL permitir que o visitante abra a tela de login da NightFall pelo botão “Login”, na rota `/login`. A tela de login SHALL oferecer um controle que retorne à página inicial.

#### Scenario: Visitante abre a tela de login
- **WHEN** o visitante ativa o botão “Login” na página inicial
- **THEN** a aplicação navega para `/login` e exibe a tela de login

#### Scenario: Visitante retorna à página inicial
- **WHEN** o visitante ativa o controle de retorno na tela de login
- **THEN** a aplicação navega de volta para a página inicial

### Requirement: Apresentação visual do formulário de login
A tela de login SHALL exibir a identidade NightFall em tema escuro com roxo como cor de destaque, além de campos identificados para e-mail e senha e um botão “Login”. O conteúdo SHALL permanecer legível e utilizável em telas estreitas e amplas, sem rolagem horizontal da página.

#### Scenario: Visitante visualiza a tela de login
- **WHEN** o visitante abre a rota `/login`
- **THEN** a tela apresenta a marca NightFall, os campos de e-mail e senha e o botão “Login” em uma interface legível

#### Scenario: Visitante acessa a tela em dispositivo estreito
- **WHEN** a tela de login é exibida em uma tela estreita
- **THEN** os campos, rótulos e controles permanecem visíveis e utilizáveis sem rolagem horizontal

### Requirement: Formulário sem autenticação ou persistência
A tela de login SHALL permitir apenas a apresentação dos campos e controles visuais. O botão “Login” do formulário SHALL NOT autenticar, validar credenciais, enviar ou armazenar dados, acessar banco de dados ou apresentar uma confirmação de login concluído.

#### Scenario: Visitante ativa o botão do formulário
- **WHEN** o visitante ativa o botão “Login” na tela de login
- **THEN** nenhuma autenticação, envio de dados, persistência ou navegação adicional é realizada
