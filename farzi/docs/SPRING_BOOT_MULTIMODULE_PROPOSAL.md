# Proposal Plan: Migration to a Multi-Module Spring Boot Architecture

## Purpose

This document proposes how to transform the current Django monolith into a structured multi-module Spring Boot system. The goal is not only framework migration, but also domain cleanup, maintainability improvement, and future production readiness.

For the target system, the proposed new product and platform name is `DecoNest`.

This is an analysis and proposal document, based on the current implementation reviewed in:

- `/Users/mantt/Documents/MCA/farzifinal/farzi/docs/EXISTING_SYSTEM_REVIEW.md`

## Executive Summary

The current system already contains multiple business domains:

- identity and role management
- product catalog and seller management
- ecommerce ordering and payments
- rental inventory and rental operations
- service booking and installation workflows
- delivery-agent onboarding and assignment
- reporting and admin operations

These domains are currently implemented inside a Django monolith with large view functions, mixed responsibilities, duplicated state, and tight coupling across apps.

A multi-module Spring Boot migration is a strong next step because it can:

- separate business domains cleanly
- move business logic into service layers
- improve testability and maintainability
- support REST-first architecture
- prepare the system for future scaling or service extraction
- make the project more production-ready and portfolio-ready

## Recommended Target Architecture

The best fit is:

- a modular monolith in Spring Boot first
- optional microservice split later if needed

This is the safest and most practical approach.

Why not jump directly to microservices:

- current domain boundaries are not clean enough yet
- there is significant shared data and duplicated logic
- payment, delivery, and booking flows still need normalization
- microservices would add deployment and distributed-data complexity too early

Recommended migration path:

1. rebuild as a multi-module Spring Boot modular monolith
2. stabilize the domain model and APIs
3. extract selected modules later only if scale or team size justifies it

## Proposed Multi-Module Structure

Suggested Maven or Gradle module structure:

- `deconest-platform`
  Parent build and dependency management
- `deconest-bootstrap`
  Main Spring Boot application launcher
- `deconest-common`
  Shared config, exceptions, constants, response wrappers, utils
- `deconest-security`
  authentication, authorization, JWT/session integration, user roles
- `deconest-user`
  users, profiles, seller profiles, delivery agent identity data
- `deconest-catalog`
  categories, subcategories, products, product media, seller product management
- `deconest-cart`
  cart, wishlist
- `deconest-order`
  orders, order items, checkout, invoice generation
- `deconest-payment`
  Razorpay integration, payment records, callback handling
- `deconest-rental`
  rental inventory, rent requests, rent lifecycle
- `deconest-service`
  service booking, maintenance, installation, appointments
- `deconest-delivery`
  delivery agent onboarding, assignment, delivery tracking
- `deconest-notification`
  email, SMS, WhatsApp, future push notifications
- `deconest-admin`
  dashboards, reporting, operational admin APIs
- `deconest-ai`
  optional furniture prediction feature

## Mapping from Current Django Apps to Spring Modules

### Current `accounts`

Map into:

- `deconest-security`
- `deconest-user`
- parts of `deconest-catalog`

Reason:

- authentication and authorization should be separated from user profile domain
- seller profile belongs to user domain
- category/product management belongs to catalog domain, not user/auth domain

### Current `main`

Map into:

- `deconest-catalog`
- `deconest-cart`
- `deconest-order`
- `deconest-payment`

Reason:

- current `main` mixes storefront browsing, cart, checkout, order, and payment logic
- these are separate business concerns and should not stay in one package

### Current `rest`

Map into:

- `deconest-rental`
- `deconest-service`
- `deconest-delivery`
- `deconest-ai`

Reason:

- the current app combines unrelated concerns
- rental, appointments, delivery agent onboarding, and AI prediction should be separate modules

### Current `serviceapp`

Map into:

- `deconest-payment`
- `deconest-delivery`
- `deconest-admin`
- `deconest-service`

Reason:

- it currently acts as an operations app, but it really contains functionality from multiple domains

## Proposed Domain Boundaries

### 1. Security Module

Responsibilities:

- login and registration
- password reset
- role-based authorization
- JWT or session-based authentication
- OAuth2 social login if retained

Current source concepts:

- `CustomUser`
- role flags
- allauth-based auth flows

Recommendation:

- move to Spring Security
- use role enums instead of scattered integer flags
- externalize OAuth support if Google login is still needed

### 2. User Module

Responsibilities:

- user profile
- seller profile
- delivery agent profile identity data
- account status management

Current source concepts:

- `UserProfile`
- `SellerProfile`
- `DeliveryAgentProfile`
- parts of `deliveryagent`

Recommendation:

- separate authentication identity from profile data
- unify repeated address/contact concepts

### 3. Catalog Module

Responsibilities:

- categories and subcategories
- products
- seller product approval and visibility
- product media references

Current source concepts:

- `Category`
- `Subcategory`
- `Product`

Recommendation:

- make this the central inventory and sale-catalog domain
- define clear product states such as `DRAFT`, `PENDING_APPROVAL`, `ACTIVE`, `INACTIVE`

### 4. Cart Module

Responsibilities:

- cart lines
- wishlist

Current source concepts:

- `BookCart`
- `Wishlist`

Recommendation:

- cart and wishlist should be simple modules with their own service layer
- avoid embedding order creation logic here

### 5. Order Module

Responsibilities:

- checkout preparation
- order creation
- order items
- order status tracking
- customer order history
- invoice generation

Current source concepts:

- `Order`
- `OrderItem`

Recommendation:

- normalize order and order item structure
- move repeated address fields into an embedded address snapshot or dedicated value object

### 6. Payment Module

Responsibilities:

- payment creation
- payment callback/webhook handling
- payment reconciliation
- payment status transitions
- payment records for sale, rent, and service

Current source concepts:

- `Payment`
- `Paymentrent`
- `Paymentservice`

Recommendation:

- replace three payment entities with either:
  - one generalized payment aggregate with payment type
  - or one shared payment base model plus typed references

Preferred design:

- a generalized `PaymentTransaction`
- linked to `ORDER`, `RENTAL`, or `SERVICE_BOOKING` by reference type

### 7. Rental Module

Responsibilities:

- rental inventory
- rental request lifecycle
- pricing and deposits
- rental availability
- rent approval/rejection

Current source concepts:

- `Furniturerent`
- `Rent`

Recommendation:

- treat rental inventory separately from sale products
- use a clearer lifecycle enum such as `REQUESTED`, `APPROVED`, `REJECTED`, `PAID`, `ASSIGNED`, `DELIVERED`, `RETURNED`

### 8. Service Module

Responsibilities:

- installation booking
- maintenance requests
- appointment slots
- service booking lifecycle

Current source concepts:

- `Appointment`
- `ServiceBooking`
- `install`

Recommendation:

- merge overlapping booking concepts where appropriate
- unify time-slot and booking status logic

### 9. Delivery Module

Responsibilities:

- delivery agent onboarding
- profile verification
- task assignment
- delivery status updates
- delivery completion

Current source concepts:

- `deliveryagent`
- `DeliveryAgentProfile`
- `Delivery`

Recommendation:

- split candidate onboarding from active delivery-agent records
- centralize assignment logic here

### 10. Notification Module

Responsibilities:

- email notifications
- SMS/WhatsApp notifications
- payment alerts
- order/rental/service status alerts

Current source concepts:

- Gmail SMTP config
- Twilio integration

Recommendation:

- keep all external messaging outside core domain modules
- publish events from core modules and let notifications subscribe

### 11. AI Module

Responsibilities:

- furniture prediction endpoint
- model loading and inference
- prediction result storage

Current source concepts:

- `FurniturePrediction`
- TensorFlow-dependent prediction views

Recommendation:

- keep this optional
- do not make application startup depend on AI dependencies

## Data Model Refactoring Analysis

The current schema should not be migrated one-to-one. It should be redesigned first.

### Key Refactoring Opportunities

- unify user-related profile entities
- normalize address handling
- unify payment records
- reduce boolean-status combinations
- separate sale-product and rental-product concepts clearly
- remove naming inconsistencies and spelling issues
- reduce repeated audit and contact fields

### Status Modeling Recommendation

Replace many-boolean states with enums.

Examples:

- `OrderStatus`
- `PaymentStatus`
- `RentalStatus`
- `BookingStatus`
- `DeliveryStatus`
- `ApprovalStatus`

This will make the Spring domain model far easier to validate and reason about.

## API Strategy Recommendation

The Spring Boot version should be API-first.

Suggested API layers:

- `controller`
- `service`
- `repository`
- `domain/entity`
- `dto/request`
- `dto/response`
- `mapper`

Suggested API grouping:

- `/api/v1/auth`
- `/api/v1/users`
- `/api/v1/sellers`
- `/api/v1/catalog`
- `/api/v1/cart`
- `/api/v1/wishlist`
- `/api/v1/orders`
- `/api/v1/payments`
- `/api/v1/rentals`
- `/api/v1/services`
- `/api/v1/delivery-agents`
- `/api/v1/admin`

## Database Recommendation

Recommended target database:

- PostgreSQL

Why:

- better production fit than SQLite
- strong Spring ecosystem support
- supports future scaling, constraints, indexing, and reporting

Migration recommendation:

- create a clean PostgreSQL schema for the Spring application
- migrate only necessary data from the Django database
- do not carry forward every historical table design decision

## Security Recommendation

Recommended target stack:

- Spring Security
- JWT-based auth for APIs
- role-based access control
- BCrypt password hashing
- OAuth2 login only if required

Immediate rule:

- no secrets in code
- all credentials in environment variables or secret management

## Build and Delivery Recommendation

Recommended stack:

- Java 21
- Spring Boot 3.x
- Maven multi-module or Gradle multi-project
- PostgreSQL
- Flyway or Liquibase for migrations
- Spring Data JPA
- MapStruct for DTO mapping
- OpenAPI/Swagger for API documentation
- Docker for containerization
- GitHub Actions for CI/CD

## Frontend Strategy Options

There are two realistic paths.

### Option A: Spring Boot backend + server-rendered templates

Good if:

- you want a simpler migration
- you want to preserve current template flow

Tradeoff:

- less modern separation
- harder to scale frontend independently

### Option B: Spring Boot backend + separate frontend

Good if:

- you want the strongest long-term architecture
- you want a portfolio-ready modern stack

Suggested frontend:

- React / Next.js

Recommendation:

- for a serious modernization proposal, choose Spring Boot backend + separate frontend
- for a lower-risk rebuild, choose Spring Boot backend first and postpone frontend rewrite

## Migration Strategy Options

### Option 1: Big-Bang Rewrite

Description:

- build the full Spring Boot system
- switch over once complete

Pros:

- clean architecture from the start

Cons:

- high risk
- long feedback cycle
- difficult testing and validation

### Option 2: Strangler Migration

Description:

- keep Django running
- rebuild one domain at a time in Spring Boot
- route features gradually

Pros:

- lower risk
- easier validation
- better for incremental delivery

Cons:

- more temporary integration work

### Recommended Choice

- use a phased rewrite with modular domain design

Since this is a two-year-old project and likely a portfolio/product rebuild rather than a live enterprise migration, a practical version is:

1. freeze Django as the reference system
2. rebuild Spring Boot modules in phases
3. migrate data selectively
4. validate each business flow one by one

## Proposed Delivery Phases

### Phase 0: Discovery and Design

Deliverables:

- current system review
- entity and flow mapping
- target module design
- API contract draft
- migration scope and priorities

### Phase 1: Foundation Setup

Deliverables:

- multi-module Spring Boot skeleton
- shared config and exception handling
- PostgreSQL schema baseline
- security baseline
- OpenAPI docs

### Phase 2: User, Security, and Catalog

Deliverables:

- auth and roles
- profiles
- seller management
- category/subcategory/product APIs

Why first:

- most other modules depend on identity and catalog

### Phase 3: Cart and Order

Deliverables:

- cart and wishlist
- checkout flow
- order and order item management
- order history

### Phase 4: Payment

Deliverables:

- Razorpay integration
- generalized payment transaction model
- callback/webhook processing

### Phase 5: Rental and Service

Deliverables:

- rental inventory and rental request lifecycle
- service booking and appointments
- installation workflows

### Phase 6: Delivery and Notifications

Deliverables:

- delivery-agent onboarding
- assignment and tracking
- email/SMS/WhatsApp notifications

### Phase 7: Reporting, Admin, and Optional AI

Deliverables:

- admin reports
- operational dashboards
- optional furniture prediction service

## Risk Analysis

### 1. Domain Confusion Risk

Risk:

- current Django apps do not map cleanly to future business modules

Mitigation:

- redesign modules around business capabilities, not old app names

### 2. Data Migration Risk

Risk:

- repeated fields and inconsistent statuses may make direct migration unreliable

Mitigation:

- define canonical Spring entities first
- migrate only validated data

### 3. Payment Flow Risk

Risk:

- payment data is spread across multiple models and flows

Mitigation:

- redesign payment into a single transactional pattern before implementation

### 4. Scope Expansion Risk

Risk:

- trying to modernize backend, frontend, AI, reporting, and deployment all at once

Mitigation:

- phase the work
- define must-have and optional scope clearly

### 5. Feature Parity Risk

Risk:

- old project contains edge-case behavior not yet documented

Mitigation:

- document each flow before rebuilding
- use Django app as behavior reference during migration

## Recommended Proposal Positioning

If you present this as a formal proposal, the message should be:

- the current project has strong business scope but weak modularity
- Spring Boot multi-module architecture will improve maintainability, scalability, testing, and deployment readiness
- the migration should be domain-driven and phased
- the first target should be a modular monolith, not immediate microservices

## Recommended Final Target

The proposed end state is:

- Spring Boot modular monolith backend
- PostgreSQL database
- API-first architecture
- separated business modules
- centralized security and payment architecture
- optional modern frontend later
- containerized deployment and CI/CD

## Suggested Next Documents

To move from proposal to execution, the next documents should be:

1. module-wise responsibility matrix
2. as-is to to-be entity mapping
3. migration phase backlog
4. API contract draft
5. database redesign proposal

## Conclusion

This project is a very good candidate for migration to a multi-module Spring Boot system because it already contains enough business scope to justify modularization. The key is to avoid a framework-only rewrite and instead use the migration to redesign the domain boundaries, normalize the data model, and establish a maintainable architecture.

The recommended path is a phased rebuild into a modular monolith, with clean business modules and strong separation of concerns. That will give the best balance of technical quality, delivery safety, and portfolio value.
