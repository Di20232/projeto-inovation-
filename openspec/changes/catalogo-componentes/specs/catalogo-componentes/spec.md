## Purpose

Define the public product-discovery experience for a computer-parts store, so visitors can browse categories and inspect product information without first creating an account.

## ADDED Requirements

### Requirement: Public catalog access
The system SHALL allow visitors to view and navigate the product catalog without signing in.

#### Scenario: Visitor opens the catalog
- **WHEN** a visitor opens the store
- **THEN** the system displays the product catalog without requiring authentication

### Requirement: Browse products by category
The system SHALL organize catalog products by category and allow visitors to view products in a selected category. Each product listing SHALL show its image, name, brand, price, and availability. Each product image SHALL have alternative text identifying the product.

#### Scenario: Visitor selects a category
- **WHEN** a visitor selects a category that contains products
- **THEN** the system displays products in that category with their image, name, brand, price, and availability

#### Scenario: Selected category has no products
- **WHEN** a visitor selects a category with no products
- **THEN** the system displays a clear empty state for that category

### Requirement: View product details
The system SHALL allow visitors to open a listed product and view its image and details, including its technical specifications.

#### Scenario: Visitor opens a product
- **WHEN** a visitor selects a product from the catalog
- **THEN** the system displays that product's image, details, and technical specifications

#### Scenario: Product is not available in the catalog
- **WHEN** a visitor requests a product that is not present in the catalog
- **THEN** the system displays a clear not-found state instead of unrelated product details
