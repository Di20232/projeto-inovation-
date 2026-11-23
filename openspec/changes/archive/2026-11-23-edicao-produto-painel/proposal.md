# Proposta: Edição de Produto no Painel Administrativo

## Contexto
A change `painel-administrativo` (17/11) registrou um modal de edição de produtos, mas o código dele nunca foi commitado: o painel só cadastrava e excluía.

## Objetivo
Permitir ao administrador editar nome, preço, categoria, marca, descrição e foto de um produto existente.

## Escopo
- Botão "Editar" em cada produto da lista do painel.
- Modal de edição pré-preenchido, com pré-visualização da foto.
- Validação: campos obrigatórios, preço numérico (aceita vírgula) e não negativo, nome sem duplicar outro produto.
- Atualizar itens do carrinho que referenciam o produto editado.
