## Context

See `proposal.md` for motivation. The storefront header is built with Reflex components in `python/python.py` and currently groups the “Categorias” dialog trigger in a horizontal header.

## Goals / Non-Goals

**Goals:**
- Add a cart-shaped icon control beside the category control and retain existing header styling and responsive behavior.
- Ensure the control is accessible while intentionally leaving it inert.

**Non-Goals:**
- Add cart state, navigation, item counts, dialog behavior, or shopping workflows.
- Add an icon package or backend changes.

## Decisions

- Use the icon component already provided by the existing Reflex icon integration and render it inside a button with a descriptive accessible label. Keep the button out of all event handlers and links so it has no action.
- Group the cart icon button and the category control in the same header row with a small consistent gap. This keeps the visual relationship clear and avoids changes to the category dialog itself.

## Risks / Trade-offs

- [The icon button may be mistaken for a working cart] → Keep the scope explicitly visual; do not add an item count, link, or interactive behavior.
- [Header controls may overflow on narrow screens] → Keep the cart icon compact and validate the existing responsive header at narrow viewport widths.
