# Proposta: Catálogo Persistente em `catalog.json`

## Contexto
O que o administrador cadastrava, editava ou excluía ficava só na memória da sessão e se perdia ao reiniciar o servidor. Os eventos que alteram o catálogo também não conferiam, no servidor, se quem chamava era admin — e a página `/admin` nem pede login.

## Objetivo
Persistir as alterações do catálogo em `python/catalog.json` com segurança.

## Escopo
- Gravação atômica do catálogo, validada pelo mesmo parser da leitura.
- Checagem de admin no servidor em cadastrar, editar e excluir (perfil e `/admin`).
- Formulários seguem as regras do parser: categoria entre as 4 da loja (lista de escolha), descrição e URL da foto obrigatórias.
- `source_url` passa a ser opcional.
- Recarregar o catálogo no `on_load` de `/`, `/perfil` e `/admin`.

## Fora do escopo
- `load_catalog` continua tentando o Xano antes do arquivo (hoje responde 404).
