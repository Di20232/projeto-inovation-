# Proposta: Verificador e Autopreenchimento de CEP via ViaCEP

## Contexto
O usuário precisa de agilidade no preenchimento do endereço de entrega no checkout, evitando digitar manualmente rua, bairro, cidade e estado.

## Objetivo
Configurar a consulta automática de CEP na API pública ViaCEP dentro do evento `set_shipping_cep` em `CatalogState`. Ao preencher 8 dígitos, o sistema busca os dados de endereço e preenche automaticamente os campos correspondentes.

## Escopo
- Formatação automática do CEP para `00000-000`.
- Requisição HTTP assíncrona para a API ViaCEP quando o CEP tiver 8 dígitos.
- Preenchimento automático de logradouro (`shipping_address`), bairro (`shipping_neighborhood`), cidade (`shipping_city`) e estado (`shipping_state`).
