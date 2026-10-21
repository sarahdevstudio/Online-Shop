# Online-Shop

A console-based online shop written in pure Python. It supports customer and admin roles, a shopping cart with discount codes, order management with a status workflow, inventory history, product reviews and an admin sales report. All data is stored in plain text files, so there is **no database and no third-party dependency**.

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Creating an admin account](#creating-an-admin-account)
- [Using the application](#using-the-application)
- [Business rules](#business-rules)
- [Project structure](#project-structure)
- [Data files](#data-files)
- [Security notes](#security-notes)
- [Known limitations](#known-limitations)

## Features

### Customers
- Register and log in (usernames are case-insensitive)
- Browse and search products by name or category
- See the average rating and number of reviews for every product
- Shopping cart: add, remove, merge quantities, stock is checked on every change
- Checkout with an optional discount code and a confirmation step
- Order history
- Product reviews: one review (1-5 stars and an optional comment) per product, only for products from a **Completed** order
- Profile: edit name, phone and address, and change the password

### Admins
- Product management: add, edit, delete, view and search
- Category management: add, view and delete
- User management: list, search, view details and edit (including role)
- Order management: list, view details and change the status following the allowed workflow
- Discount codes: create (percentage and maximum number of uses), list and delete
- Sales report: revenue, order counts by status, top selling products, sales by category and low-stock alerts

### Behind the scenes
- Inventory history for every stock change (initial stock, sales, cancellations and manual edits)
- Cancelling an order returns its items to stock
- Deleting a product also removes it from all carts and removes its reviews
- Input validation for numbers, phone numbers, usernames and passwords
- Salted password hashing (PBKDF2-HMAC-SHA256); old SHA-256 hashes are upgraded automatically on login
- The last remaining admin cannot be demoted

## Requirements

- Python 3.8 or newer (developed and tested on 3.12)
- No external packages

## Getting started

```bash
git clone <repository-url>
cd Online-Shop
python main.py
```

The data files are resolved relative to the project folder, so the application can be started from any working directory, for example `python path/to/Online-Shop/main.py`.

The repository ships with sample categories, products, discount codes, users and one order in the `data/` folder. Look at `data/users.txt` for the seeded accounts. Passwords are stored only as hashes.

## Creating an admin account

Registration always creates a normal user. To create an admin, run this once from the project folder:

```bash
python -c "from services.auth_service import AuthService as A; print(A.create_admin('myadmin', 'a-strong-password', 'My Name', '09120000000', 'My address'))"
```

An existing user can also be promoted from **Admin menu → Users Management → Edit User**.

## Using the application

### Main menu

```
1. Register
2. Login
3. Exit
```

### User menu

```
1. View Products          6. Remove Product from Cart
2. Search Product         7. Checkout
3. View Categories        8. Order History
4. Add Product to Cart    9. My Profile
5. View Cart              10. Product Reviews
                          11. Logout
```

### Admin menu

```
1. Add Product            7. Order Management
2. Edit Product           8. Discount Management
3. Delete Product         9. Category Management
4. View Products          10. Sales Report
5. Search Product         11. Logout
6. Users Management
```

### A typical flow

1. A customer registers, logs in, adds products to the cart and checks out (optionally with a discount code).
2. The order is created with the status **Pending** and the stock is reduced.
3. An admin moves the order through **Processing → Shipped → Completed**.
4. After the order is **Completed**, the customer can rate and review the purchased products.

## Business rules

### Order status workflow

| From | Allowed next status |
|------|---------------------|
| Pending | Processing, Cancelled |
| Processing | Shipped, Cancelled |
| Shipped | Completed |
| Completed | none |
| Cancelled | none |

When an order becomes **Cancelled**, every item is returned to stock and a `CANCEL` record is added to the inventory history.

### Discount codes
- A code has a percentage (greater than 0 and at most 100) and a maximum number of uses
- Codes are case-insensitive and unique
- A code is rejected if it does not exist, is inactive or has reached its usage limit
- The usage counter increases only when an order is actually placed

### Inventory history operations

| Operation | When it is recorded |
|-----------|---------------------|
| `STOCK_IN` | A product is added with a stock greater than zero |
| `SALE` | Checkout |
| `CANCEL` | An order is cancelled |
| `ADJUST` | An admin changes the stock while editing a product |

### Reviews
- Rating from 1 to 5, with an optional comment
- Only users who have a **Completed** order containing the product can review it
- Writing a second review for the same product replaces the first one

### Sales report
- Cancelled orders are excluded from revenue and from sales statistics
- Low stock means 5 units or fewer
- Order lines do not store the price at purchase time, so per-product statistics are counted in units, not in money

## Project structure

```
Online-Shop/
├── main.py                  # entry point
├── menus/
│   ├── main_menu.py         # register / login / exit
│   ├── user_menu.py         # customer menus (cart, checkout, profile, reviews)
│   └── admin_menu.py        # admin menus (products, users, orders, discounts, report)
├── models/                  # plain data classes
│   ├── user.py  product.py  category.py  cart.py
│   ├── order.py  discount.py  inventory_record.py  review.py
├── services/                # business logic and file persistence
│   ├── auth_service.py
│   ├── product_service.py
│   ├── category_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   ├── discount_service.py
│   ├── inventory_service.py
│   ├── review_service.py
│   └── report_service.py
├── utils/
│   ├── file_manager.py      # read / write / append helpers
│   ├── password_helper.py   # salted password hashing
│   ├── validators.py        # input validation rules
│   └── helpers.py           # interactive input helpers
└── data/                    # text-file "database"
```

The code is layered: **menus** talk only to **services**, services use **models** and `FileManager`, and `utils` contains shared helpers.

## Data files

Every file lives in `data/`, has one record per line and uses `|` as the field separator. For that reason the `|` character is not accepted in any user input.

| File | Format |
|------|--------|
| `users.txt` | `id\|username\|password_hash\|name\|phone\|address\|role` |
| `products.txt` | `id\|name\|category\|price\|stock` |
| `categories.txt` | `id\|name` |
| `carts.txt` | `user_id\|product_id\|quantity` |
| `orders.txt` | `id\|user_id\|product_id,qty;product_id,qty\|total\|status\|discount_code\|discount_amount` |
| `discounts.txt` | `id\|code\|percent\|max_uses\|used_count\|active` |
| `inventory_history.txt` | `id\|product_id\|change\|operation\|note\|created_at` |
| `reviews.txt` | `id\|product_id\|user_id\|rating\|comment\|created_at` |

Malformed lines are skipped when reading, so a damaged line never crashes the application.

## Security notes

- Passwords are hashed with PBKDF2-HMAC-SHA256 using a random 16-byte salt and 100,000 iterations. They are stored as `salt$hash`.
- Accounts created with the older unsalted SHA-256 hash can still log in and are upgraded to the new format on their first successful login.
- The data files are plain text. Do not commit real customer data and protect the `data/` folder if you deploy the project.

## Known limitations

- The storage layer is not safe for concurrent use: two instances writing the same files at the same time can overwrite each other
- Prices are not stored in order lines, so changing a product price later does not change old orders, but old orders also cannot show per-item prices
- Users cannot cancel their own orders; only admins can change the order status
- There are no automated tests yet

## Possible next steps

- Switch the storage layer to SQLite
- Pagination, sorting and filtering for the product list
- Let customers cancel their own pending orders and export invoices
- CSV export for products, orders and users
- Temporary account lock after repeated failed logins
- Unit tests for the services and validators
