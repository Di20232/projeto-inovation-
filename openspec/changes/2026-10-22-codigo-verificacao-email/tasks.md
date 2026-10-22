# Tasks: Verificação Real de E-mail

## 1. Especificação e contrato
- [x] 1.1 Documentar requisitos de verificação server-side, não exposição do código, falha de envio, expiração, tentativas e política de acesso pendente.
- [x] 1.2 Registrar lacunas comprovadas no contrato Xano existente; não inferir endpoints ou sintaxe.

## 2. Cliente Reflex: remover falsa verificação
- [x] 2.1 Remover geração e comparação local do código e a mensagem que o expunha como simulação.
- [x] 2.2 Não afirmar envio nem confirmação de e-mail; informar que a verificação ainda não está disponível.
- [ ] 2.3 Implementar etapa de confirmação quando o contrato backend estiver definido e publicado.

## 3. Backend Xano e SendGrid — pendente
- [ ] 3.1 Definir contrato de signup pendente, desafio, confirmação e resposta segura.
- [ ] 3.2 Definir armazenamento protegido do código, expiração, tentativas, reenvio e invalidação.
- [ ] 3.3 Implementar envio no backend com variáveis protegidas do SendGrid; tratar falhas sem marcar conta verificada.
- [ ] 3.4 Bloquear login/acesso verificado para conta pendente conforme política acordada.
- [ ] 3.5 Configurar credenciais no workspace Xano sem inseri-las no repositório.
- [ ] 3.6 Publicar os endpoints e validar recebimento e confirmação com endereço de teste autorizado.

## 4. Validação local
- [ ] 4.1 Testar respostas do cliente com transporte HTTP mockado, sem chamadas externas.
- [ ] 4.2 Executar `reflex compile --dry` e registrar o resultado.
