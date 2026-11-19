## Why

Os cards de produto exibem informações e preço, mas não têm um destaque visual semelhante ao de lojas virtuais para a opção de compra. Um botão verde “Comprar +” em cada produto ajuda a comunicar esse padrão sem introduzir um fluxo de carrinho nesta etapa.

## What Changes

- Exibir um botão verde com o texto “Comprar +” em cada card de produto mostrado no catálogo.
- Manter o botão estritamente visual: ativá-lo não adiciona itens, altera estado, navega ou abre os detalhes do produto.
- Preservar o acesso atual aos detalhes do produto e manter o botão utilizável em telas estreitas.

## Capabilities

### New Capabilities

### Modified Capabilities
- `identidade-inicial-loja`: Definir a exibição e o comportamento inerte do botão “Comprar +” nos cards de produtos reais.

## Impact

- Cards de produto na página inicial em `python/python.py`.
- Spec de `identidade-inicial-loja`.
- Sem alterações em APIs, banco de dados, estado de carrinho, dependências ou rotas.
