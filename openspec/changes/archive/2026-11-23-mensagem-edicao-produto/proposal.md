# Proposta: Mensagem curta na edição de produto

## Contexto
Ao salvar a edição de um produto no painel, `save_edited_product` mostrava "Produto 'X' atualizado e salvo no catálogo!".

## Objetivo
Trocar o aviso final por um texto curto: "Produto atualizado.".

## Escopo
- Uma linha em `CatalogState.save_edited_product` (`python/python.py`).

## Fora do escopo
- Mensagens de cadastro e exclusão continuam como estão.
