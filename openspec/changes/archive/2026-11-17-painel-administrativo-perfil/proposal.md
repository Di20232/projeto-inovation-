# Proposal: Painel Administrativo Exclusivo

## Why
O sistema NightFall precisa de um painel administrativo acessível exclusivamente pelo usuário administrador (`admin@admin.com`, senha `admin123`) na página de perfil (`/perfil`), permitindo gerenciar produtos (adicionar, editar preço, nome, descrição, categoria e marca) e marcas diretamente na interface.

## What Changes
- Adicionar autenticação especial para `admin@admin.com` / `admin123` definindo `is_admin = True`.
- Adicionar a aba "Gerenciar Site" na página de perfil exclusiva para administradores.
- Implementar formulários e lógica no `CatalogState` / `AuthState` para adicionar novos produtos, editar produtos existentes e gerenciar marcas/categorias.
- Criar change OpenSpec e documentar as especificações.
