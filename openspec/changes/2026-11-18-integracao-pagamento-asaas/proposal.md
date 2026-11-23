# Proposta: Integração de Pagamento com Asaas

## Motivo
Permitir pagamentos reais ou via sandbox na loja virtual NightFall utilizando o gateway Asaas (Pix e Cartão de Crédito).

## Escopo
- Criação do serviço `asaas_service.py` para comunicação com a API do Asaas.
- Configuração de chave de API e ambiente (`ASAAS_API_KEY`, sandbox/production).
- Atualização do fluxo de checkout para criar cliente e cobrança no Asaas.
- Exibição de QR Code Pix e dados de pagamento ao concluir o pedido.
