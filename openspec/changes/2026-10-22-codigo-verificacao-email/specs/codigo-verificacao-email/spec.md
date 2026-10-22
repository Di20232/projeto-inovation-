## Purpose

Verificar a posse do endereço de e-mail após o cadastro por meio de um código numérico de 5 dígitos, com geração, envio e confirmação confiáveis no backend.

## ADDED Requirements

### Requirement: Código de verificação gerado e enviado pelo backend
O sistema SHALL gerar um código de 5 dígitos no backend e enviá-lo ao endereço informado usando o provedor configurado. O código SHALL NOT ser exposto ao cliente, incluído em respostas, logs ou interface. O backend SHALL guardar somente uma representação protegida do código, com expiração e limite de tentativas.

#### Scenario: Cadastro e pedido de envio aceitos
- **WHEN** uma pessoa envia dados válidos para cadastro e o backend aceita o envio de e-mail
- **THEN** o sistema informa que o código foi enviado, sem revelar o código, e mantém a conta pendente de verificação

#### Scenario: Envio de e-mail falha
- **WHEN** o provedor de e-mail recusa ou não aceita a solicitação de envio
- **THEN** o sistema não afirma que o código foi enviado nem que o e-mail foi verificado, e retorna uma resposta de falha segura

### Requirement: Confirmação da verificação no backend
O sistema SHALL confirmar o código no backend e marcar a conta como verificada somente após validação bem-sucedida. Códigos incorretos, expirados, usados ou excedendo o limite de tentativas SHALL ser rejeitados sem alterar a conta para verificada.

#### Scenario: Código válido
- **WHEN** a pessoa submete um código válido e ainda não expirado para o desafio correspondente
- **THEN** o backend invalida o desafio e marca o endereço de e-mail como verificado

#### Scenario: Código incorreto ou expirado
- **WHEN** a pessoa submete um código incorreto, expirado ou já utilizado
- **THEN** o backend rejeita a confirmação, não verifica o endereço e retorna mensagem que não expõe segredos

### Requirement: Conta não verificada não recebe acesso verificado
O sistema SHALL manter contas pendentes sem acesso que dependa de e-mail verificado, conforme o contrato de autenticação definido para signup, login e recursos autenticados.

#### Scenario: Login de conta pendente
- **WHEN** uma conta ainda não confirmou o e-mail tenta autenticar ou acessar recurso protegido
- **THEN** o sistema aplica a política documentada para conta pendente sem conceder acesso de conta verificada

## Implementation status

Os endpoints Xano atuais não implementam estes requisitos. A integração, os contratos, o deploy e a validação com provedor permanecem pendentes; o fluxo cliente atualmente disponível não constitui verificação real.
