# Design: Integração Asaas

## Arquitetura
1. `asaas_service.py`: gerencia chamadas HTTP para `https://api.asaas.com/v3` (ou sandbox `https://sandbox.asaas.com/api/v3`).
2. Mapeamento de dados do cliente logado (`AuthState`) e carrinho para o payload do Asaas.
3. Tratamento de erros e retorno de dados de cobrança (Pix QrCode, payload, status).
