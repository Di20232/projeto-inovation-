# Spec: Garantia dos produtos

## Requisitos
- O cadastro e a edição de produto permitem informar a garantia em meses, de 0 a 120. Vazio ou 0 significa sem garantia.
- Valor fora desse intervalo ou não inteiro é recusado com mensagem, sem salvar o produto.
- Cada pedido guarda o prazo de garantia vigente na compra.
- A aba "Garantia" lista os produtos com garantia comprados pelo cliente logado, com pedido, data da compra, prazo, validade e situação.
- Um cliente não vê a garantia de outro.
- Sem nenhum produto com garantia, a aba explica que eles aparecem depois da compra.
