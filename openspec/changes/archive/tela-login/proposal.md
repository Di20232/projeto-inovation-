## Why

A página inicial da NightFall já oferece um botão “Login”, mas ainda não existe uma tela de destino. Criar uma tela de login visual e acessível completa esse caminho de navegação sem antecipar autenticação ou persistência de dados.

## What Changes

- Adicionar uma tela de login da NightFall acessível pela rota `/login`.
- Fazer o botão “Login” da página inicial navegar para essa rota.
- Apresentar campos de e-mail e senha e um botão de login somente como elementos visuais, sem processar credenciais nem autenticar.
- Manter a identidade visual escura e roxa da loja e oferecer um caminho de retorno à página inicial.

## Capabilities

### New Capabilities
- `login-screen`: tela de login apenas visual, sua navegação a partir da página inicial e retorno à página inicial.

### Modified Capabilities
- Nenhuma. A navegação até a nova tela faz parte da capacidade `login-screen`.

## Impact

- Afeta a página inicial e as rotas/componentes da aplicação Reflex.
- Não adiciona APIs, autenticação, acesso a banco de dados, armazenamento de credenciais ou dependências.
