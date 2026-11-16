# Proposta: Data de Nascimento no Padrão Brasileiro (DD/MM/YYYY)

## Contexto
Atualmente, os campos de data de nascimento utilizavam o input HTML nativo `type="date"`, que impõe o formato ISO (YYYY-MM-DD) e exibe barras/ordem dependendo da localidade do navegador, o que diverge do padrão brasileiro (DD/MM/YYYY) utilizado nos formulários de cadastro e perfil do NightFall.

## Objetivo
Padronizar a entrada da data de nascimento nos formulários de cadastro (`/cadastro`) e perfil (`/perfil` -> Meus Dados) para o formato brasileiro `DD/MM/YYYY`, com formatação automática ao digitar e placeholder adequado.

## Escopo
- Criação da função utilitária `format_birth_date` para formatar os dígitos no padrão `DD/MM/YYYY`.
- Atualização do `RegistrationState` e `AuthState` para utilizar a formatação.
- Substituição de `type="date"` por input textual formatado nas páginas de cadastro e perfil.
- Documentação da especificação em OpenSpec.
