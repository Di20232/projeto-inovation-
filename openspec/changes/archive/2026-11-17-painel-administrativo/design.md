# Design: Painel Administrativo Completo

## Arquitetura e Componentes
- **AdminState**: Novo estado Reflex em `python/python.py` que gerencia a aba ativa (`admin_tab`), campos para cadastro de novos produtos (`new_prod_*`) e mensagens de feedback (`admin_message`).
- **admin_page()**: Componente principal da rota `/admin` estilizado com o tema dark cyberpunk do NightFall (`#0b0b12`, `#a78bfa`, efeitos em vidro).
- **Abas**:
  - `produtos`: Tabela/lista de produtos existentes com opção de remoção.
  - `adicionar_produto`: Formulário para inclusão de novos hardwares/periféricos.
  - `pedidos`: Listagem de pedidos dos clientes.
  - `clientes`: Listagem de clientes da plataforma.
