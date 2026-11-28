# Proposta: Garantia dos produtos

## Contexto
A aba "Garantia" do perfil mostrava sempre um texto fixo dizendo que não havia produtos. Não existia onde cadastrar o prazo de garantia.

## Objetivo
O administrador cadastra a garantia do produto e o cliente vê, na aba "Garantia", os produtos comprados que têm garantia.

## Escopo
- Campo "Garantia (meses)", de 0 a 120, no cadastro (Perfil > Gerenciar Site e `/admin`) e na edição de produto.
- Gravar o prazo no catálogo e em cada item do pedido.
- Aba "Garantia" com produto, número do pedido, data da compra, prazo, validade e situação (Ativa ou Expirada).

## Fora do escopo
- Publicar o campo em uma tabela do Xano.
- Preencher prazos nos produtos já existentes: quem define é o administrador.
- Acionamento ou solicitação de garantia pelo cliente.
