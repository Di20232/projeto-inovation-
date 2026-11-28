# Tarefas: Integração Asaas

- [x] Criar módulo `asaas_service.py` <!-- id: 1 -->
- [ ] Atualizar `python/python.py` para integrar o checkout com o Asaas <!-- id: 2 -->
- [x] Documentar configuração da chave de API do Asaas <!-- id: 3 -->
- [x] Validar compilação e execução <!-- id: 4 -->

## Validação (2026-11-23)

- **1:** `asaas_service.py` existe (commit 607f52f), mas nenhum arquivo o importa. O checkout usa funções próprias em `python/python.py` (`find_asaas_customer`, `create_asaas_customer`, `find_asaas_payment`) com outra URL de sandbox (`api-sandbox.asaas.com/v3` contra `sandbox.asaas.com/api/v3` no módulo). Hoje o módulo é código morto.
- **2 (aberta):** a integração com cartão existe e `test_asaas_checkout.py` passa (3 testes), mas a chamada real ao Sandbox não foi exercida (não há `ASAAS_API_KEY` no `.env`), e Pix com QR Code, que está no escopo da proposta, não foi feito: o checkout responde "Pix e boleto ainda não estão integrados ao Asaas".
- **3:** documentado no `README.md` (seção "Integração de Pagamento (Asaas Sandbox)") e no `.env.example` (`ASAAS_API_KEY`, `NIGHTFALL_SIMULATED_PAYMENTS`).
- **4:** `reflex compile --dry` passou; checkout ponta a ponta no navegador em modo simulado (sem `ASAAS_API_KEY`) criou o pedido `#NF-9C7A4738` (R$ 164,90, status "Simulado (sem cobrança)") no `orders_db.json`.
