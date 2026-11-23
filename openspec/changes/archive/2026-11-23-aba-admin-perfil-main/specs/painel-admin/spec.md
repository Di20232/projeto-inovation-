# Spec: Painel Administrativo (perfil)

## Requisitos
- A aba "Gerenciar Site" do `/perfil` aparece somente para usuário com `is_admin = True`.
- O logout zera `is_admin`; um login comum feito em seguida não vê a aba.
