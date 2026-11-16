# Proposta: Cadastro de Múltiplos Endereços e Seleção de Endereço Principal

## Contexto
Na seção de perfil (`/perfil` -> Endereços), havia apenas um endereço estático simulado ("Praça da Sé"), sem possibilidade de cadastrar novos endereços ou definir qual deles é o endereço principal de entrega.

## Objetivo
Permitir que o usuário cadastre múltiplos endereços, edite/remova e selecione qual endereço é o principal na sua conta.

## Escopo
- Adição de estrutura de dados `addresses` e formulário de novo endereço no `AuthState`.
- Implementação de ações para adicionar endereço, alternar formulário, definir endereço principal e excluir endereço.
- Atualização da aba "Endereços" na página de perfil (`/perfil`) com listagem dinâmica, botão de novo endereço, badge de principal e opções de gerenciamento.
- Documentação da especificação em OpenSpec.
