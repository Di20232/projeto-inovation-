## Purpose
Garantir que após efetuar o login, o usuário seja redirecionado para a página inicial e a interface reflita seu nome na barra superior.

## ADDED Requirements

### Requirement: Redirecionamento e estado de sessão após login
O sistema SHALL atualizar o estado de autenticação com os dados do usuário e redirecionar para a página inicial (`/`) imediatamente após um login bem-sucedido.

#### Scenario: Login bem-sucedido
- **WHEN** o usuário preenche credenciais válidas e clica em entrar
- **THEN** o sistema autentica a sessão, define o nome do usuário e redireciona para `/`

### Requirement: Exibição do nome do usuário na barra superior
A barra superior da página inicial SHALL exibir o nome do usuário autenticado no lugar do botão de login.

#### Scenario: Usuário autenticado visualiza seu nome
- **WHEN** um usuário logado acessa a página inicial
- **THEN** o botão de login é substituído pelo nome do usuário
