# Spec: Catálogo persistente

## Requisitos
- Cadastrar, editar e excluir pelo painel grava em `python/catalog.json` e persiste após reiniciar o servidor.
- Uma alteração inválida não altera o arquivo.
- Somente administrador logado pode alterar o catálogo; caso contrário a operação é recusada com mensagem.
- A categoria deve ser uma de: Computadores, Componentes, Periféricos, Acessórios.
