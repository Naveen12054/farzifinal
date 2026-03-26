# DecoNest Backend

This directory contains the new `DecoNest` backend, rebuilt as a multi-module Spring Boot project.

## Modules

- `deconest-bootstrap`: Spring Boot application entrypoint
- `deconest-common`: shared exceptions, utilities, constants, base config
- `deconest-security`: authentication and authorization
- `deconest-user`: users, profiles, seller profile, account management
- `deconest-catalog`: categories, subcategories, products, inventory metadata
- `deconest-cart`: cart and wishlist
- `deconest-order`: checkout, orders, order items, invoices
- `deconest-payment`: payment orchestration and gateway integration
- `deconest-rental`: rental inventory and rental lifecycle
- `deconest-service`: service booking, appointments, installation and maintenance
- `deconest-delivery`: delivery agent onboarding, assignment and tracking
- `deconest-notification`: email, SMS, WhatsApp and event-driven notifications
- `deconest-admin`: admin reporting and operational endpoints
- `deconest-ai`: optional AI and furniture prediction features

## Planned Stack

- Java 17+
- Spring Boot 3.3.x
- Maven multi-module build
- PostgreSQL
- Flyway
- Spring Security
- Spring Data JPA

## Next Steps

1. Define shared architecture conventions across modules.
2. Add domain entities and repositories module by module.
3. Introduce security, persistence, and API foundations.
4. Implement business flows in phases, starting with user and catalog.
