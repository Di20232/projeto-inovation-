# Proposta: Página de Perfil do Usuário

## Contexto
Os usuários autenticados na plataforma NightFall precisam de uma área dedicada para visualizar e gerenciar suas informações cadastrais (nome, e-mail).

## Objetivo
Implementar a página de perfil (`/perfil`) na aplicação Reflex (`python/python.py`), permitindo que usuários logados visualizem seus dados, atualizem seu nome de exibição e acessem a página de forma protegida por autenticação.

## Escopo
- Rota dedicada `/perfil` com layout responsivo e tema escuro NightFall.
- Link direto no cabeçalho (clicando no nome do usuário logado) para acesso rápido ao perfil.
- Proteção de autenticação (Auth Guard): redirecionamento para login caso o usuário acesse sem estar autenticado.
- Edição de nome de exibição com feedback visual de sucesso.
