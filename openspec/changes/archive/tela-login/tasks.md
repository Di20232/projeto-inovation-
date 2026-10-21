## 1. Tela de login

- [x] 1.1 Criar a página Reflex na rota `/login` com identidade visual NightFall, campos identificados de e-mail e senha, botão visual “Login” e controle de retorno para `/`; verificar os elementos e a navegação declarativa na página.
- [x] 1.2 Garantir que os campos e o botão de formulário não tenham manipuladores, validação/autenticação, envio ou persistência de dados; verificar que ativar “Login” não autentica nem apresenta confirmação.

## 2. Integração e validação

- [x] 2.1 Transformar o botão “Login” da página inicial em navegação para `/login`, preservando o estilo visual existente; verificar que a ativação abre a rota correta.
- [x] 2.2 Validar a compilação com `reflex compile --dry` e verificar visualmente as rotas `/` e `/login` em telas estreitas e amplas, sem rolagem horizontal.
