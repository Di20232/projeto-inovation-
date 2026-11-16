## Purpose

Puxar as informações e imagens dos produtos diretamente do Xano, com suporte a fallback local.

## ADDED Requirements

### Requirement: Consulta de produtos no Xano
O sistema SHALL buscar os dados dos produtos a partir de um endpoint REST do Xano (`XANO_PRODUCTS_URL`), populando o catálogo dinamicamente.

#### Scenario: Xano retorna produtos com sucesso
- **WHEN** a aplicação inicializa e consegue conectar ao Xano (`XANO_PRODUCTS_URL`)
- **THEN** o catálogo exibe os produtos vindos do Xano (imagens, preços, descrições e especificações)

#### Scenario: Xano indisponível ou não configurado
- **WHEN** a URL do Xano não está configurada ou o serviço falha
- **THEN** o sistema realiza o fallback para o arquivo local `catalog.json`, garantindo que o site continue funcionando
