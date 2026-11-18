# Tarefas: Remoção de Dados Fixos de Pedidos e Garantia no Perfil

- [x] Adicionar listas `orders` e `warranties` vazias em `AuthState`
- [x] Integrar `finalize_order` para popular `AuthState.orders` com dados reais do checkout
- [x] Atualizar renderização da aba "Meus Pedidos" com `rx.cond` e `rx.foreach` baseados no estado real
- [x] Atualizar renderização da aba "Garantia" para exibir estado vazio adequado
- [x] Validar compilação do código Python
