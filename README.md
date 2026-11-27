# NightFall — Loja Virtual de Tecnologia e Computadores

Aplicação web full-stack desenvolvida em **Python** com o framework **Reflex**, com backend e banco de dados via **Xano**, pagamentos via **Asaas (Sandbox)** e estilização com Tailwind v4 e Radix Themes.

---

## 🚀 Funcionalidades Principais

- **Catálogo de Produtos** (`/`): computadores, hardware e acessórios com busca dinâmica e filtros avançados (preço e marca).
- **Autenticação** (`/cadastro`, `/login`): cadastro com validação de CPF e data de nascimento no formato brasileiro (`DD/MM/YYYY`). O login usa o Xano quando `XANO_LOGIN_URL` está configurada; sem ela, funciona um login local de desenvolvimento.
- **Perfil** (`/perfil`):
  - **Meus Dados**: visualização e atualização de nome, e-mail, CPF e data de nascimento.
  - **Endereços**: múltiplos endereços, com preenchimento automático por CEP (**ViaCEP**).
  - **Meus Pedidos**: histórico e status dos pedidos.
- **Carrinho** (`/carrinho`) e **Checkout** (`/pagamento`): cupons promocionais, exigência de endereço de entrega completo antes de criar o pedido e pagamento com cartão via Asaas Sandbox.
- **Painel Administrativo** (`/admin`): gestão de produtos e pedidos, acessível apenas a administradores verificados no servidor.
- **Persistência de pedidos**: pedidos gravados no Xano (`order_persistence.py`, `xano_orders_setup.py`, ver `xano-orders-docs.md`).

### Autenticação

Por padrão, contas são salvas em `auth_users.sqlite3`; senhas são armazenadas somente como hashes PBKDF2-SHA256 e cada e-mail pode ser cadastrado uma única vez. Configure `NIGHTFALL_AUTH_DB` para apontar o banco a um volume persistente no ambiente de hospedagem. O Xano é opcional: para usá-lo como fonte de autenticação, publique os endpoints de cadastro e login e configure `XANO_SIGNUP_URL` e `XANO_LOGIN_URL`. Falhas no login do Xano não liberam acesso localmente.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend & Backend**: Python 3, [Reflex](https://reflex.dev) v0.9.12
- **Estilização**: Tailwind CSS v4 e Radix Themes
- **Banco de Dados / API**: [Xano](https://www.xano.com) (schemas `.xs`)
- **Pagamentos**: Asaas (Sandbox)
- **CEP**: API ViaCEP
- **Fluxo de mudanças**: OpenSpec (`openspec/`)

---

## 🗂️ Estrutura do Projeto

| Caminho | Descrição |
|---|---|
| `python/python.py` | App Reflex: estados, páginas e rotas |
| `python/catalog.json` | Catálogo local de produtos |
| `admin_auth.py` | Verificação de administrador no servidor |
| `asaas_service.py` | Integração com o Asaas |
| `order_persistence.py` | Persistência de pedidos no Xano |
| `scripts/gerar_hash_admin.py` | Gera o hash da senha do admin |
| `seed_xano_products.py` | Popula produtos no Xano |
| `xano/nightfall-user-auth/` | API de autenticação do Xano (`signup`, `login`, `me`) e tabela `usuario` |
| `table/`, `api/`, `function/` | Schemas e endpoints Xano (`.xs`) |
| `openspec/` | Specs e propostas de mudança |
| `projeto/docs/` | Visão geral e modelo de domínio |

---

## 📦 Como Executar o Projeto Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Di20232/projeto-inovation-.git
   cd projeto-inovation-
   ```

2. **Crie e ative o ambiente virtual e instale as dependências**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1      # Windows (PowerShell)
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**: copie `.env.example` para `.env` e preencha (veja a seção abaixo).

4. **Inicie a aplicação**:
   ```bash
   reflex run
   ```

5. **Acesse no navegador**: `http://localhost:3000/` (o backend usa a porta `8003`).

---

## ⚙️ Variáveis de Ambiente (`.env`)

| Variável | Para que serve |
|---|---|
| `XANO_SIGNUP_URL` | Endpoint de cadastro no Xano |
| `XANO_PRODUCTS_URL` | Endpoint de produtos no Xano |
| `XANO_LOGIN_URL` | Endpoint de login no Xano. Vazio = login local de desenvolvimento |
| `ADMIN_EMAIL` | E-mail do administrador local |
| `ADMIN_PASSWORD_HASH` | Hash PBKDF2-SHA256 da senha do admin |
| `ASAAS_API_KEY` | Chave do **Sandbox** do Asaas |
| `NIGHTFALL_SIMULATED_PAYMENTS` | `1` (padrão) usa pagamento simulado em localhost quando não há `ASAAS_API_KEY`; `0` desliga |

Reinicie o Reflex depois de alterar o `.env`.

---

## 🔐 Administrador

A credencial do admin **não fica no código**. O acesso é decidido no servidor por:

- **Admin local (`.env`)**: `ADMIN_EMAIL` + `ADMIN_PASSWORD_HASH`. Gere o hash sem exibir a senha com:
  ```bash
  python scripts/gerar_hash_admin.py
  ```
  Sem essas duas variáveis, ninguém é admin pelo `.env`.
- **Xano**: campo `is_admin` na tabela `usuario`; o login devolve `authToken` e `user.is_admin`. Depende de publicar os `.xs` de `xano/nightfall-user-auth/` no workspace do Xano.

O cadastro nunca concede admin e o logout limpa o token.

---

## 💳 Integração de Pagamento (Asaas Sandbox)

- Configure `ASAAS_API_KEY` no `.env` com uma chave do Sandbox.
- O formulário de cartão cria/usa o cliente e registra uma cobrança de teste no Asaas.
- Use somente cartões fictícios de teste; o Sandbox não movimenta dinheiro.
- Os dados do cartão não são salvos pelo NightFall. HTTPS é obrigatório fora do localhost.
- Pix e boleto ainda não estão integrados.

---

## 🧪 Testes Automatizados Locais

```bash
python test_app_local.py        # rotas da aplicação
python tests_unitarios.py       # testes unitários
python tests_admin_auth.py      # autenticação de admin
python test_asaas_checkout.py   # checkout com Asaas
```

`test_xano_live.py` e `test_xano_orders.py` chamam o Xano real e exigem as variáveis configuradas.

---

## 📄 Licença
Projeto desenvolvido para fins educacionais e e-commerce de demonstração.
