# Painel administrativo: aviso ao salvar edição

## Requisito: aviso de edição salva
Ao salvar a edição de um produto com sucesso, o painel SHALL mostrar o aviso "Produto atualizado.".

### Cenário: edição válida
- **Dado** um administrador logado na aba "Gerenciar Site"
- **Quando** ele edita um produto e clica em "Salvar Alterações"
- **Então** o catálogo é gravado e o aviso "Produto atualizado." aparece
