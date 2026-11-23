## Context

See `proposal.md` for motivation and `specs/identidade-inicial-loja/spec.md` for the observable behavior. Product cards currently use a button for opening product details, so the new visual control must not be nested inside or activate that button.

## Goals / Non-Goals

**Goals:**
- Preserve the existing product-details interaction while presenting the purchase-styled control beside the product information.
- Keep the control independently focusable and inert.

**Non-Goals:**
- Implement cart data, add-to-cart actions, checkout, or product availability changes.

## Decisions

- Render the card content and its controls in a non-interactive layout container, with the existing details trigger and the “Comprar +” button as siblings. This avoids invalid nested buttons and prevents activating the visual purchase button from bubbling into the details action.
- Use the existing Reflex button component with a green style and visible “Comprar +” text. Give it an accessible name that includes the product name, set its type to `button`, and do not attach an event handler, link, or state.
- Keep the control within the card's responsive content flow so it can wrap naturally on narrow screens. Do not add dependencies.

## Risks / Trade-offs

- [A purchase-styled control may imply a working cart] → Keep it explicitly inert and exclude counts, cart updates, navigation, and checkout.
- [The existing card uses a button for its details interaction] → Separate the details trigger and purchase button as siblings rather than nesting interactive elements.
