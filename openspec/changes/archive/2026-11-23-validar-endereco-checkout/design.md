# Design

- Função pura `missing_shipping_fields(cep, endereco, numero, bairro, cidade, uf) -> list[str]` em `python/python.py`, que devolve os nomes dos campos faltando ou inválidos.
- `CatalogState._shipping_problem()` monta a mensagem a partir dela; `finalize_order` e `_finalize_simulated_order` param com `payment_message` se houver problema.
- Testes em `tests_unitarios.py`.
