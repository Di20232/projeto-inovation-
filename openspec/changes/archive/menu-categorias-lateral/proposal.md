## Why

A página inicial da NightFall ainda não oferece uma forma de explorar as categorias da futura loja. Um menu lateral introduz uma navegação clara agora, enquanto indica que cada categoria está em preparação até haver produtos disponíveis.

## What Changes

- Adicionar um menu lateral deslizante acionado por um controle de categorias na página inicial.
- Apresentar as categorias Computadores, Componentes, Periféricos e Acessórios.
- Exibir o estado “Em breve” para as categorias enquanto o catálogo não tiver produtos, sem criar produtos fictícios ou sugerir que a navegação por produtos já está disponível.
- Permitir abrir e fechar o menu com interações acessíveis e mantê-lo utilizável em telas estreitas e amplas.

## Capabilities

### New Capabilities

### Modified Capabilities
- `identidade-inicial-loja`: ampliar a página inicial pública com navegação lateral por categorias e estados de categoria em preparação.

## Impact

- Página inicial Reflex em `python/python.py`.
- Especificação existente em `openspec/specs/identidade-inicial-loja/`.
- Nenhuma fonte de produtos, API, banco de dados, dependência ou integração com Xano será adicionada.
