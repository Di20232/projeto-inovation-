# Proposta: Remoção de Dados Fixos de Pedidos e Garantia no Perfil

## Visão Geral
Remover os dados mockados/fixos (pedido `#NF-84920` e garantia do processador Ryzen 7) que apareciam no perfil do usuário ao criar conta ou fazer login, implementando a dinâmica correta onde os pedidos só aparecem quando efetuados no checkout.

## Objetivos
1. Inicializar `orders` e `warranties` como listas vazias em `AuthState`.
2. Registrar o pedido real no estado do usuário (`AuthState.orders`) durante a execução de `finalize_order`.
3. Ajustar a renderização na `profile_page` para exibir os pedidos reais do usuário ou uma mensagem de vazio quando não houver compras.
4. Ajustar a aba "Garantia" para exibir mensagem informativa quando não houver produtos com garantia registrada.
