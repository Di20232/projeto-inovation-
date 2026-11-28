# Design

- `discount_amount` passa a ser `@rx.var`, calculada por `coupon_discount(subtotal, applied)` com arredondamento em centavos.
- `_reset_coupon` é usada ao remover o cupom, esvaziar o carrinho e registrar o pedido.
- `AuthState.save_profile` valida com `profile_problem` e grava com `auth_persistence.save_profile`, que já existia no repositório e não era chamada.
- No login, o perfil salvo vale mais que o cadastro ou o Xano. Sem dados salvos, CPF e data ficam vazios.
- Conta com data inválida gravada antes precisa corrigir a data para salvar.
