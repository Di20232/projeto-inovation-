## Purpose

Enviar um código de verificação numérico de 5 dígitos aleatórios para o e-mail do usuário após o login ou cadastro, exigindo a inserção do código para confirmar a identidade.

## ADDED Requirements

### Requirement: Geração e envio de código de 5 dígitos
O sistema SHALL gerar um código numérico aleatório de 5 dígitos e enviá-lo/exibi-lo para validação pós-login ou pós-cadastro.

#### Scenario: Usuário conclui login/cadastro e recebe código
- **WHEN** o usuário submete com sucesso as credenciais no login ou os dados no cadastro
- **THEN** o sistema avança para a tela de verificação de código e gera um código aleatório de 5 dígitos para o e-mail

#### Scenario: Usuário confirma código correto
- **WHEN** o usuário digita o código de 5 dígitos correto recebido por e-mail
- **THEN** o acesso à aplicação ou conclusão da conta é efetivado com sucesso

#### Scenario: Usuário digita código incorreto
- **WHEN** o usuário digita um código incorreto
- **THEN** o sistema exibe mensagem de erro e impede o avanço
