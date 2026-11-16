# Design: Cadastro de Múltiplos Endereços e Seleção de Endereço Principal

## Arquitetura
- **Estado (`AuthState`)**:
  - `addresses`: lista de dicionários contendo `id`, `title`, `street`, `number`, `complement`, `neighborhood`, `city`, `state`, `cep`, `is_main`.
  - Campos do formulário: `is_adding_address`, `new_address_title`, `new_address_cep`, `new_address_street`, `new_address_number`, `new_address_complement`, `new_address_neighborhood`, `new_address_city`, `new_address_state`, `address_message`.
  - Eventos: `toggle_add_address_form`, `add_address`, `set_main_address`, `delete_address` e setters dos campos.
- **Interface**:
  - Aba "Endereços" em `/perfil`: botão para adicionar novo endereço, formulário expansível, cartões dinâmicos de endereços com botão "Tornar Principal" e "Remover".

## Verificação
- Testar cadastro de múltiplos endereços.
- Testar definição de endereço principal e remoção.
