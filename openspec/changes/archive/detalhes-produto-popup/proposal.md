## Why

O catálogo já permite explorar produtos e filtrar por categoria, mas os cards não oferecem espaço suficiente para consultar suas especificações técnicas. Um pop-up de detalhes permite conhecer melhor cada item sem sair da listagem.

## What Changes

- Tornar cada card de produto acionável para abrir um pop-up com imagem, nome, categoria, preço, descrição e especificações técnicas.
- Organizar as especificações em campos legíveis e compatíveis com as diferentes categorias de produtos.
- Permitir fechar o pop-up pelo controle de fechamento, pela tecla Escape ou pela área externa, mantendo o conteúdo utilizável em telas estreitas.
- Não incluir link para a loja, galeria de imagens, carrinho ou fluxo de compra.

## Capabilities

### New Capabilities

### Modified Capabilities
- `identidade-inicial-loja`: adicionar a abertura e o fechamento acessível de detalhes para os produtos exibidos no catálogo.

## Impact

- Página inicial Reflex em `python/python.py` para interação dos cards e apresentação do pop-up.
- `python/catalog.json` para registrar as especificações técnicas dos produtos sem substituir os dados já existentes.
- Especificação principal de identidade e navegação da loja.
- Nenhuma API, banco de dados, dependência externa ou integração com Xano será adicionada.
