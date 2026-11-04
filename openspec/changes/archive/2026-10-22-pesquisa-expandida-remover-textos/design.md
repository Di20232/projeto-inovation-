# Design: Remover textos e expandir barra de pesquisa no foco

## Layout
- Remover o bloco de texto introdutório da página inicial (`index`).
- A barra de pesquisa passa a ocupar o topo da área de conteúdo, com largura total (`width="100%"`) e transição suave no foco.
- Efeito de foco: aumentar a altura levemente, sombra mais destacada (`box_shadow="0 0 0 2px #a78bfa, 0 8px 30px rgba(139, 92, 246, 0.25)"`) e transição em `all 0.25s ease`.

## Estrutura
- `index` chama diretamente o grid de catálogo (com categorias ao lado e produtos).
- Barra de pesquisa no topo com tamanho dinâmico e responsivo.
