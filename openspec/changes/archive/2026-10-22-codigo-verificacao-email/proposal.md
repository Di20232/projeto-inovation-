# Proposta: Verificação Real de E-mail

## Contexto
O fluxo atual gera e valida um código no cliente Reflex e o exibe na interface como simulação. Isso não comprova que a pessoa controla o endereço de e-mail. Os endpoints Xano existentes neste repositório não implementam envio nem confirmação de códigos.

## Objetivo
Implementar verificação pós-cadastro com decisão confiável no backend: o Xano gera e armazena o desafio de forma segura, envia o código pelo SendGrid e confirma o código antes de marcar o e-mail como verificado. O cliente nunca gera, recebe ou exibe o código.

## Escopo
- Definir contrato de signup, confirmação e estado de conta não verificada.
- Gerar código numérico de 5 dígitos no backend, guardar representação protegida com expiração e política contra tentativas abusivas.
- Enviar e-mail pelo SendGrid usando configuração protegida no workspace Xano.
- Confirmar o código no backend e impedir login/ações protegidas para contas não verificadas, de acordo com o contrato de autenticação.
- Tratar falhas de envio, código inválido/expirado e respostas sem expor segredo.
- Validar com mocks e, após configuração e publicação, com um endereço de teste autorizado.

## Estado
A implementação backend, configuração/deploy do Xano e validação do recebimento são pendentes. A simulação no cliente não deve ser considerada verificação concluída.
