# Design

- `_catalog_cache` (lista viva do processo) + `threading.Lock`.
- `mutate_catalog(change)`: aplica a mudança sobre o cache, valida com `parse_catalog_data`, grava em arquivo temporário + `os.replace`; se for inválida, não altera arquivo nem cache.
- `build_product(...)`: monta e valida um produto do formulário (lança `ValueError` com mensagem para o usuário).
- `CatalogState._is_admin()`: lê `AuthState` (logado e admin). `AdminState` reutiliza a mesma checagem.
- Removido `update_product` (sem uso e sem checagem).
- Commit: `a96537c`.
