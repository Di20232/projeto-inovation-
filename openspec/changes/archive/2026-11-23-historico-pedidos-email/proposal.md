# Proposta: Histórico de Pedidos por E-mail

## Contexto
"Meus Pedidos" mostrava só os pedidos da sessão atual: depois de reiniciar o servidor ou logar de novo, a lista ficava vazia. O logout também não limpava a lista, então o próximo usuário no mesmo navegador via o histórico do anterior.

## Objetivo
Mostrar ao cliente todos os seus pedidos salvos, e só os dele.

## Escopo
- Ler o `orders_db.json` filtrando pelo `user_email`.
- Carregar no login, no cadastro e ao abrir o `/perfil`.
- Limpar a lista no logout.
