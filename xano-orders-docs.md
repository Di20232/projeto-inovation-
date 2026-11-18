# Documentação: Configuração do Endpoint Orders no Xano

## Status Atual
O cadastro de usuários (`/signup`) já funciona perfeitamente e salva dados no Xano. Porém, o endpoint `/orders` ainda não foi criado no painel Xano, o que impede a persistência dos pedidos no banco de dados.

## Endpoints Existentes (Funcionando)

| Endpoint | Descrição | Status |
|----------|-----------|--------|
| `https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/signup` | Cadastro de novo usuário | ✅ Funcionando |
| `https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/produto` | CRUD de produtos | ✅ Funcionando |

## Endpoint Necessário (Não criado)

### `https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/orders`

## Campos Obrigatórios para o Endpoint Orders

No painel Xano, ao criar uma nova tabela/tipo de dado para `orders`, os seguintes campos são necessários:

### Campos do Usuário
| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| `user_email` | Texto (String) | ✅ Sim |
| `payment_method` | Texto (String) | ✅ Sim |
| `status` | Texto (String) | ✅ Sim |

### Campos do Pedido
| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| `items` | JSON (Array) | ✅ Sim |
| `subtotal` | Número (Number) | ✅ Sim |
| `discount` | Número (Number) | ✅ Sim |
| `shipping` | Número (Number) | ✅ Sim |
| `total` | Número (Number) | ✅ Sim |
| `shipping_address` | JSON (Objeto) | ✅ Sim |

### Campos Opcionais
| Campo | Tipo |
|-------|------|
| `order_id` | Texto (String) |
| `created_at` | Data/Hora |

## JSON Structure Esperado para o Campo `items`

```json
[
  {
    "name": "Produto Nome",
    "price": 123.45,
    "quantity": 2
  }
]
```

## JSON Structure Esperado para o Campo `shipping_address`

```json
{
  "cep": "01001-000",
  "address": "Praça da Sé",
  "number": "100",
  "neighborhood": "Sé",
  "city": "São Paulo",
  "state": "SP"
}
```

## Como Configurar no Painel Xano

1. Acesse o painel Xano: https://manage.xano.io
2. Selecione o workspace do projeto NightFall
3. Crie uma nova **Table/Datasource** chamada `orders`
4. Adicione os campos listados acima (user_email, payment_method, status, items, subtotal, discount, shipping, total, shipping_address)
5. Marque os campos obrigatórios com o ícone de asterisco (*)
6. Salve a tabela

Após criar a tabela, configure o **Endpoint API**:
7. Vá em **API Endpoints** → **Create Endpoint**
8. Selecione **POST** method
9. Escolha a tabela `orders` que você criou
10. Defina o caminho como `/orders` (ou deixar como padrão)
11. Salve e teste com o payload abaixo

## Payload de Teste para o Endpoint POST /orders

```json
POST https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/orders

{
  "user_email": "teste.user@exemplo.com",
  "items": [
    {
      "name": "Processador AMD Ryzen 7 7800X3D",
      "price": 2899.90,
      "quantity": 1
    }
  ],
  "subtotal": 2899.90,
  "discount": 289.99,
  "shipping": 0.0,
  "total": 2609.91,
  "shipping_address": {
    "cep": "01001-000",
    "address": "Praça da Sé",
    "number": "100",
    "neighborhood": "Sé",
    "city": "São Paulo",
    "state": "SP"
  },
  "payment_method": "credit_card",
  "status": "pending"
}
```

## Próximos Passos Após Configuração

1. Teste o endpoint manualmente via Postman ou curl
2. Reinicie o aplicativo Reflex (`reflex run`)
3. Realize um checkout no NightFall
4. Verifique se o pedido aparece no painel Xano e no perfil do usuário (`/perfil` → aba "Meus Pedidos")

## Arquivos Relacionados

- `test_xano_orders.py` - Teste existente que retorna 404 até a tabela ser criada
- `python/python.py` - Integração do `finalize_order()` com `AuthState.orders`