## Why

A aplicação Reflex está em uma tela mínima e ainda não apresenta a identidade da NightFall nem uma entrada reconhecível para a futura loja. Uma página inicial com tema escuro e estado vazio comunica a marca sem sugerir que já existem produtos, preços ou funções de catálogo disponíveis.

## What Changes

- Criar a primeira interface pública da NightFall usando Reflex, preservando a tecnologia e a estrutura atuais do aplicativo.
- Apresentar o nome da loja com uma identidade visual predominantemente preta e roxa, mantendo contraste e legibilidade.
- Exibir um estado vazio claro informando que o catálogo está sendo preparado, sem produtos de demonstração, preços, filtros ou ações de compra.
- Manter a página inicial simples e preparada visualmente para evolução futura, sem antecipar integrações de dados.

## Capabilities

### New Capabilities
- `identidade-inicial-loja`: identidade visual e estado inicial vazio da página pública da NightFall.

### Modified Capabilities

## Impact

- Página inicial Reflex em `python/python.py`.
- Nenhuma mudança em APIs, banco de dados, dependências ou workspace Xano.
