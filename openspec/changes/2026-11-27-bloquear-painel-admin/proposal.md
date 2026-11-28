# Proposta: Bloquear o painel administrativo

## Contexto
Em 2026-11-27 a página `/admin` abria o painel para visitantes. As alterações de produto já eram recusadas no servidor, mas a tela aparecia.

## Objetivo
Mostrar o painel só a administradores.

## Escopo
- Quem não é administrador vê "Acesso Restrito", com os links de login e de volta à loja.

## Fora do escopo
- Os textos fixos das abas "Pedidos" e "Clientes" continuam no código e no JavaScript enviado ao navegador.
- A aba "Gerenciar Site" do perfil.
