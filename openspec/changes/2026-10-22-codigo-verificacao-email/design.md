# Design: Verificação Real de E-mail

## Limite de confiança
O código e o estado de verificação pertencem ao backend. O cliente Reflex apenas solicita cadastro, coleta o código digitado e apresenta a resposta do servidor. Nunca gerar código no cliente nem retorná-lo em resposta HTTP, estado Reflex, logs ou interface.

## Fluxo proposto
1. O signup cria uma conta pendente e solicita ao backend o envio de um desafio de 5 dígitos.
2. O backend gera o código com fonte apropriada, guarda somente representação protegida com prazo de validade e limite de tentativas, e envia por SendGrid usando `sendgrid_api_key` e `sendgrid_from_email` configurados como variáveis protegidas do workspace.
3. A resposta ao signup confirma somente que o pedido de envio foi aceito; falha de envio deve ser explícita e não pode ser apresentada como e-mail verificado.
4. A confirmação recebe identificador de desafio e código digitado, compara no servidor, rejeita códigos incorretos ou expirados e marca a conta como verificada somente após sucesso.
5. O login e recursos autenticados devem respeitar o estado não verificado conforme o contrato de autenticação definido pelo projeto.

## Contratos a definir antes da implementação
- Identificador de desafio, formato das entradas e respostas e códigos HTTP.
- Campos/tabela de desafios, armazenamento protegido, expiração, tentativas máximas, reenvio e invalidação após uso.
- Política de falha/transação para conta pendente quando a entrega falhar.
- Bloqueio de login/token e comportamento de usuários já existentes.
- Integração com a função SendGrid disponível e teste de caixa postal autorizada.

O repositório contém helpers SendGrid, mas não comprova a sintaxe de geração de código numérico nem esses contratos; não implementar endpoint Xano por inferência.

## Cliente Reflex
Remover a simulação local. Até existir contrato publicado, não mostrar tela de código, nem afirmar que um e-mail foi enviado/verificado. Após contrato definido, configurar URLs públicas do endpoint no ambiente e tratar sucesso, falha, código incorreto e expiração sem expor dados sensíveis.

## Segurança e validação
Não armazenar chaves no repositório ou frontend. Usar mocks locais para testar os contratos após sua definição. A validação real exige configuração protegida no Xano, endpoints publicados e recebimento em endereço de teste autorizado.
