# Design: Código de Verificação por E-mail (5 Dígitos)

## Arquitetura
- **Estado**: Estados de autenticação (`LoginState`, `RegistrationState` ou novo estado de verificação) geram um código de 5 dígitos (`random.randint(10000, 99999)`).
- **Interface**: Tela de verificação de código com campo de entrada de 5 dígitos e botão de confirmação.

## Verificação
- Garantir que o código gerado tenha exatamente 5 dígitos numéricos.
- Validar se a tela de confirmação aceita o código correto e rejeita incorretos.
