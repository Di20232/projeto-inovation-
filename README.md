# NightFall — Loja Virtual de Tecnologia e Computadores

Aplicação web full-stack desenvolvida em **Python** utilizando o framework **Reflex**, com integração de backend e banco de dados via **Xano** e estilização moderna com Tailwind v4 e Radix Themes.

---

## 🚀 Funcionalidades Principais

- **Catálogo de Produtos**: Exibição de computadores, hardware e acessórios com busca dinâmica e painel de filtros avançados (preço e marca).
- **Autenticação de Usuários**: Fluxo completo de cadastro (`/cadastro`) e login (`/login`), com validação de CPF e formatação brasileira de data de nascimento (`DD/MM/YYYY`).
- **Gerenciamento de Perfil (`/perfil`)**:
  - **Meus Dados**: Visualização e atualização de nome, e-mail, CPF e data de nascimento.
  - **Endereços**: Gerenciamento de múltiplos endereços com preenchimento automático por CEP (**ViaCEP**).
  - **Meus Pedidos**: Histórico de compras e status de pedidos.
- **Carrinho e Checkout**: Carrinho de compras dedicado, aplicação de cupons promocionais e fluxo de pagamento com validação de endereço.
- **Segurança e Persistência**: Schemas de banco de dados estruturados para persistir dados de usuários e endereços.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend & Backend**: Python 3, [Reflex](https://reflex.dev) v0.9.12
- **Estilização**: Tailwind CSS v4 & Radix Themes
- **Banco de Dados / API**: Xano (`.xs` schemas)
- **Integração de CEP**: ViaCEP API
- **Arquitetura de Mudanças**: OpenSpec

---

## 📦 Como Executar o Projeto Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Di20232/projeto-inovation-.git
   cd projeto-inovation-
   ```

2. **Ative o ambiente virtual (`venv`)**:
   - No Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

3. **Inicie a aplicação Reflex**:
   ```bash
   reflex run
   ```

4. **Acesse no navegador**:
   - `http://localhost:3000/` (ou `http://localhost:3001/`)

---

## 🧪 Testes Automatizados Locais

Para executar os testes automatizados de rotas:
```python
python test_app_local.py
```

---

## 📄 Licença
Projeto desenvolvido para fins educacionais e e-commerce de demonstração.
