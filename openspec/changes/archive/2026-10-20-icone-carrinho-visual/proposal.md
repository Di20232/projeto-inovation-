## Why

The storefront header currently has a categories control but no visual indication of the shopping-cart area. Adding a simple cart icon beside that control makes the familiar storefront element visible while keeping the requested scope limited to presentation.

## What Changes

- Add a visually styled shopping-cart icon button adjacent to the “Categorias” button in the storefront header.
- Give the icon an accessible label and preserve the existing responsive layout.
- Keep the button intentionally non-functional: it does not navigate, open a panel, update a count, or alter cart data.

## Capabilities

### New Capabilities

### Modified Capabilities
- `identidade-inicial-loja`: Add an accessible, visual-only cart control to the storefront header.

## Impact

- The storefront header in `python/python.py`.
- No backend, database, cart behavior, new dependency, or route changes.
