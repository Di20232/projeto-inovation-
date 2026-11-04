# Proposta: Integração do Catálogo de Produtos com o Xano

## Contexto
O catálogo de produtos da NightFall é carregado atualmente de um arquivo local (`catalog.json`). O backend Xano possui estrutura para gerenciar produtos, mas o site ainda não consome dados de lá.

## Objetivo
Fazer com que a aplicação NightFall busque as informações e imagens dos produtos diretamente do Xano (`XANO_PRODUCTS_URL`), mantendo `catalog.json` como fallback seguro caso o endpoint esteja indisponível.

## Escopo
- Configuração da variável de ambiente `XANO_PRODUCTS_URL`.
- Implementação de requisição HTTP na inicialização/carregamento do catálogo para puxar produtos do Xano.
- Tratamento de falhas com fallback para o catálogo local.
