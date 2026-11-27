# Proposta: Login com Enter e Campos Limpos

## Contexto
Na tela `/login`, apertar Enter não envia o formulário: só o botão "Entrar" funciona. Além disso, o `LoginState` guarda o e-mail e a senha digitados mesmo quando o login não é enviado. Ao voltar para `/login`, os campos aparecem vazios, mas o estado ainda tem o valor antigo, e um pedido de teste saiu gravado com o e-mail duplicado (`cliente.teste@exemplo.comcliente.teste@exemplo.com`).

## Objetivo
Enviar o login com Enter e garantir que o que aparece nos campos é o que o servidor usa.

## Escopo
- Enter no campo de e-mail ou de senha dispara o mesmo login do botão "Entrar".
- Ao abrir `/login`, o e-mail, a senha e a mensagem são zerados no estado.

## Fora do escopo
- Mudar as regras de autenticação (`admin_auth.py`).
