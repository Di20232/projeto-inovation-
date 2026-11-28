# Proposta: Corrigir cupom e salvar do perfil

## Contexto
Nos testes de 2026-11-27:
- O desconto do cupom ficava fixo no valor do momento da aplicação (R$ 14,99 sobre R$ 449,70) e continuava na tela depois da compra.
- "Salvar Alterações" mostrava sucesso sem gravar; ao entrar de novo, os dados antigos voltavam.

## Objetivo
O desconto sempre corresponder ao carrinho e os dados do perfil permanecerem salvos.

## Escopo
- Desconto de 10% calculado a partir do carrinho; cupom removido ao fechar o pedido ou esvaziar o carrinho.
- Salvar nome, CPF e data de nascimento no banco local, com validação, e carregá-los no login.

## Fora do escopo
- Salvar endereços e telefone.
- Gravar o perfil no Xano.
- Validar a data de nascimento no cadastro.
