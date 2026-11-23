# Design

- `CatalogState`: campos `edit_*`, `edit_dialog_open`, `edit_error`; eventos `open_edit_product` e `save_edited_product`.
- A marca é a especificação `Marca` (`specifications`), que alimenta o filtro de marcas.
- UI: `admin_edit_product_dialog()` renderizado uma vez na aba admin; `admin_product_row` ganhou o botão "Editar".
- Commit: `6f047b7`.
