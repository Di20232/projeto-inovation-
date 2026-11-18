# Design: Remoção de Dados Fixos de Pedidos e Garantia no Perfil

## Arquitetura e Alterações
- **AuthState**:
  - `orders: list[dict] = []` (inicia vazia).
  - `warranties: list[dict] = []` (inicia vazia).
- **finalize_order()**:
  - Ao finalizar o pedido com sucesso, adiciona um dicionário contendo ID gerado, data atual, quantidade de itens, total formatado e status "Concluído" no histórico do usuário (`auth_state.orders`).
- **profile_page()**:
  - Aba "Meus Pedidos": Utiliza `rx.cond` em `AuthState.orders.length() > 0` para exibir a lista com `rx.foreach` ou a mensagem "Você ainda não realizou nenhum pedido na NightFall.".
  - Aba "Garantia": Exibe aviso de que os hardwares adquiridos em pedidos concluídos aparecerão ali.
