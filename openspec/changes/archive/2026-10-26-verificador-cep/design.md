# Design: Verificador e Autopreenchimento de CEP

## Arquitetura e Decisões
- **API Externa**: ViaCEP (`https://viacep.com.br/ws/{cep}/json/`).
- **Estado**: `CatalogState.set_shipping_cep` processa o valor digitado, formata o CEP com hífen e faz chamada assíncrona com `httpx`.
- **Autopreenchimento**: Atualiza diretamente `shipping_address`, `shipping_neighborhood`, `shipping_city` e `shipping_state`.
