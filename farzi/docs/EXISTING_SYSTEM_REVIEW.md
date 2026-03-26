 # Existing System Review

## Project Summary

This project is a Django-based multi-module web application for a furniture business. The system combines:

- product catalog and ecommerce ordering
- seller-side product management
- furniture rental workflows
- service booking and installation workflows
- delivery-agent onboarding and assignment flows
- payment handling through Razorpay
- authentication through custom email-based login and Google social login

The current Django project name is `soulcure`, while the business/domain naming in the code and templates is largely `Farzi`. For the migration and modernization effort, the proposed new product/platform name is `DecoNest`. The codebase reflects an organically grown academic/project system with multiple business areas implemented in a single monolith.

## Tech Stack

- Backend framework: Django 4.x
- Database: SQLite for local development, optional `DATABASE_URL` support for external databases
- Authentication: custom `CustomUser` model + `django-allauth`
- Admin theme: `django-jazzmin`
- Payments: Razorpay
- Messaging: Twilio / WhatsApp integration
- PDF generation: `xhtml2pdf`
- Media/static handling: Django static and media directories
- Frontend: Django templates with static CSS/JS assets

## High-Level Architecture

The application is structured as a monolithic Django project with four primary apps:

- `accounts`
  Purpose: authentication, profile management, seller management, category/product admin functions
- `main`
  Purpose: storefront, catalog, cart, wishlist, checkout, order and payment flows
- `rest`
  Purpose: rental listings, installation/service requests, delivery-agent registration, appointment management, furniture prediction feature
- `serviceapp`
  Purpose: rental/service payment flows, delivery assignment, admin dashboards, compare feature, feedback

Project entry points:

- Root router: `/Users/mantt/Documents/MCA/farzifinal/farzi/soulcure/urls.py`
- Settings: `/Users/mantt/Documents/MCA/farzifinal/farzi/soulcure/settings.py`
- Main templates folder: `/Users/mantt/Documents/MCA/farzifinal/farzi/templates`
- Static assets: `/Users/mantt/Documents/MCA/farzifinal/farzi/static`
- Uploaded media: `/Users/mantt/Documents/MCA/farzifinal/farzi/media`

## URL Structure

The root URL router mounts the apps like this:

- `/admin/` -> Django admin
- `/` -> `main` app
- `/accounts/` -> `accounts` app
- `/rest/` -> `rest` app
- `/serviceapp/` -> `serviceapp` app

### Main User-Facing Areas

- Storefront and product pages: `main.urls`
- Login, registration, seller profile, admin dashboard: `accounts.urls`
- Rental and service booking pages: `rest.urls`
- Rental/service payment and delivery operations: `serviceapp.urls`

## Core Domain Modules

### 1. Accounts Module

Files:

- `/Users/mantt/Documents/MCA/farzifinal/farzi/accounts/models.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/accounts/views.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/accounts/urls.py`

Main responsibilities:

- custom email-based authentication
- user registration and login
- customer, seller, delivery, admin role distinction
- user profile and seller profile maintenance
- category and product management from seller/admin workflows

Main models:

- `CustomUser`
  Central identity model with role support
- `UserProfile`
  Customer address/contact information
- `SellerProfile`
  Seller business/contact details
- `Category`
  Product grouping with rent/sale flags
- `Subcategory`
  Secondary product grouping
- `Product`
  Core sale product entity with images, price, stock, and metadata

Observations:

- `CustomUser` replaces username with email as the login identifier
- Role handling is embedded in integer flags
- Product management logic exists directly in views instead of a dedicated service layer

### 2. Main Ecommerce Module

Files:

- `/Users/mantt/Documents/MCA/farzifinal/farzi/main/models.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/main/views.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/main/urls.py`

Main responsibilities:

- homepage and catalog browsing
- product detail pages
- cart and wishlist handling
- checkout and order creation
- order listing and sales reporting
- Razorpay payment initiation and payment callbacks
- PDF invoice/export endpoint

Main models:

- `BookCart`
  Cart items linked to user and product
- `Wishlist`
  Saved products for later
- `Order`
  Order summary and customer address data
- `Payment`
  Razorpay-backed ecommerce payment record
- `OrderItem`
  Individual purchased items

Observations:

- Product purchase flow and payment flow are tightly coupled inside large view functions
- `Order` and `OrderItem` overlap in responsibility and contain repeated address/order information
- There are multiple payment-related paths and at least one duplicated function name in `main/views.py`

### 3. Rental and Service Base Module

Files:

- `/Users/mantt/Documents/MCA/farzifinal/farzi/rest/models.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/rest/views.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/rest/urls.py`

Main responsibilities:

- rental product listings
- rental request creation
- service and installation request intake
- delivery agent registration and approval flows
- appointment scheduling
- furniture image prediction feature

Main models:

- `FurniturePrediction`
  Stores uploaded image and predicted class
- `install`
  Installation booking record
- `Addressuser`
  Address book for users
- `Furniturerent`
  Rental inventory item
- `Rent`
  Rental request / rental transaction
- `deliveryagent`
  Delivery candidate entity
- `DeliveryAgentProfile`
  Delivery profile data
- `Appointment`
  Appointment-based service request
- `ServiceBooking`
  Generic service booking record

Observations:

- This app contains several unrelated concerns grouped together
- Naming is inconsistent, for example `install`, `deliveryagent`, `manintenece`
- The furniture prediction feature depends on optional ML libraries and is not isolated from the main app structure conceptually

### 4. Service Operations Module

Files:

- `/Users/mantt/Documents/MCA/farzifinal/farzi/serviceapp/models.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/serviceapp/views.py`
- `/Users/mantt/Documents/MCA/farzifinal/farzi/serviceapp/urls.py`

Main responsibilities:

- rental payment flow
- service payment flow
- compare products feature
- delivery assignments
- delivery completion
- admin operational dashboards
- user feedback for services/products

Main models:

- `Paymentrent`
  Payment records for rental orders
- `CompareProduct`
  User compare list
- `Paymentservice`
  Payment records for service bookings
- `Delivery`
  Delivery assignment state
- `Feedback`
  Product/service feedback storage

Observations:

- `serviceapp` acts as an operations layer but still contains business logic directly in views
- Delivery and admin dashboard logic would benefit from clearer domain separation

## Main Business Flows Present in the System

### User and Seller Flow

1. User registers or logs in through email-based auth
2. User may maintain profile information
3. Seller creates seller profile
4. Seller/admin manages categories and products

### Ecommerce Purchase Flow

1. Customer browses products
2. Customer adds items to cart or wishlist
3. Customer checks out and creates an order
4. Razorpay payment is initiated
5. Payment callback updates records
6. Customer can review order history

### Rental Flow

1. User browses furniture available for rent
2. User selects rental period and address
3. Admin reviews rental requests
4. Rental payment is processed through Razorpay
5. Delivery/assignment status is updated

### Service / Installation Flow

1. User requests service, maintenance, or installation
2. Appointment or service booking is recorded
3. Admin/provider reviews requests
4. Payment may be collected through service payment flow
5. Delivery/service completion is tracked

### Delivery Agent Flow

1. Delivery agent expresses interest or registers
2. Profile is created and reviewed
3. Admin accepts or rejects
4. Delivery agent receives assignments
5. Delivery completion is tracked

## Existing Data Model Themes

The system stores several categories of data:

- identity and role data
- seller and customer profile data
- sale product catalog data
- rental inventory and rental transaction data
- service booking and appointment data
- payment transaction data
- delivery assignment data
- feedback and comparison data

There is visible duplication across these areas, especially:

- address fields repeated across multiple models
- payment handling implemented separately for product, rental, and service
- status represented through many booleans rather than a single lifecycle field

## Current Configuration State

From the current settings file:

- local development defaults to SQLite
- external DB can be supplied via `DATABASE_URL`
- static and media files are served from project folders
- Google social auth is enabled in installed apps
- SMTP email, Razorpay, and Twilio credentials are currently hardcoded in settings

## Known Technical Risks and Review Notes

This section focuses on current-state review findings rather than future redesign.

### Security and Configuration Risks

- Sensitive credentials are committed directly in `/Users/mantt/Documents/MCA/farzifinal/farzi/soulcure/settings.py`
- `DEBUG = True` and `ALLOWED_HOSTS = ['*']` are not production-safe
- Email, payment, and Twilio config should be environment-driven

### Maintainability Risks

- Business logic is concentrated in very large function-based views
- App boundaries are blurred, especially in `rest` and `serviceapp`
- Naming is inconsistent and sometimes misspelled
- There are duplicate imports and repeated code patterns in URL/view files

### Data Modeling Risks

- Multiple models repeat the same address and status data
- Status handling uses many booleans, which can create conflicting states
- Some method names use `str` instead of `__str__`, which limits admin/debug usefulness
- Cross-app coupling is high

### Feature Robustness Risks

- Payment, PDF, ML, and messaging features rely on external libraries/services without strong isolation
- Import-time dependencies can affect startup if not guarded
- Some optional features are not currently resilient when dependencies are missing

## What This System Already Demonstrates Well

Even with technical debt, the project already shows meaningful breadth:

- custom auth model
- multi-role workflows
- ecommerce ordering
- rental domain logic
- service booking logic
- payment integration
- delivery operations
- admin-oriented reporting/dashboard concepts

This gives the project strong portfolio potential once cleaned up and documented properly.

## Recommended Immediate Documentation Follow-Ups

This review should be followed by:

1. module-by-module functional documentation
2. database/entity relationship documentation
3. current route inventory
4. setup and run guide
5. known issues and refactor backlog

## Review Scope

This document is a first-pass architectural and functional review based on the current code structure in the repository. It is intended to help understand the existing system before making changes. It is not yet a full API spec, ER diagram, or user manual.
