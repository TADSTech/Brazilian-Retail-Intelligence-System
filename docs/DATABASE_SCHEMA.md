# Database Schema

PostgreSQL (Supabase in production, local Postgres for development).
Models: `db_schema/models.py`. FK/index tooling: `db_schema/setup_constraints.py`.

## Tables

### `customers`
| Column | Type | Constraints |
|---|---|---|
| customer_id | text | PK |
| customer_unique_id | text | |
| customer_zip_code_prefix | text | |
| customer_city | text | |
| customer_state | text | full state name |
| customer_state_initials | text | UF code |

### `geolocation`
| Column | Type | Constraints |
|---|---|---|
| geolocation_id | integer | PK, generated |
| geolocation_zip_code_prefix | integer | |
| geolocation_lat / lng | double precision | |
| geolocation_city / state | text | |
| geolocation_state_initials | text | |

### `orders`
| Column | Type | Constraints |
|---|---|---|
| order_id | text | PK |
| customer_id | text | NOT NULL, FK → customers |
| order_status | text | NOT NULL |
| order_purchase_timestamp | timestamp | |
| order_approved_at | timestamp | |
| order_delivered_carrier_date | timestamp | |
| order_delivered_customer_date | timestamp | |
| order_estimated_delivery_date | timestamp | |

### `order_items`
| Column | Type | Constraints |
|---|---|---|
| order_id | text | PK part, FK → orders |
| order_item_id | integer | PK part |
| product_id | text | NOT NULL, FK → products |
| seller_id | text | NOT NULL, FK → sellers |
| shipping_limit_date | timestamp | |
| price / freight_value | double precision | |

### `order_payments`
| Column | Type | Constraints |
|---|---|---|
| order_id | text | PK part, FK → orders |
| payment_sequential | integer | PK part |
| payment_type | text | NOT NULL |
| payment_installments | integer | NOT NULL |
| payment_value | double precision | NOT NULL |

### `order_reviews`
| Column | Type | Constraints |
|---|---|---|
| order_id | text | PK, FK → orders |
| review_id | text | one review per order (enforced in transform) |
| review_score | integer | |
| review_comment_title / message | text | |
| review_creation_date / answer_timestamp | timestamp | |

### `products`
| Column | Type | Constraints |
|---|---|---|
| product_id | text | PK |
| product_category_name | text | Portuguese |
| product_category_name_english | text | from `product_category_name_translation.csv` |
| product_name_lenght, product_description_lenght, product_photos_qty | integer | |
| product_weight_g, product_length_cm, product_height_cm, product_width_cm | integer | |

### `sellers`
| Column | Type | Constraints |
|---|---|---|
| seller_id | text | PK |
| seller_zip_code_prefix | integer | |
| seller_city | text | |
| seller_state | text | full name |
| seller_state_initials | text | |

## Relationships

```text
customers ──< orders ──< order_items >── products
                   ├──< order_payments        │
                   └──< order_reviews         └──< sellers
```

Load order (parents first): `geolocation → customers → sellers → products → orders → order_items → order_payments → order_reviews`.

## Indexes

Created by `python -m db_schema.setup_constraints`:

- FK columns: `orders.customer_id`, `order_items.order_id/product_id/seller_id`, `order_payments.order_id`, `order_reviews.order_id`
- Query paths: `orders.order_status`, `orders.order_purchase_timestamp`, `products.product_category_name`

The setup script is idempotent (checks `pg_constraint` and `pg_indexes` first).

## Local setup

```bash
ETL_BACKEND=postgres DATABASE_URL=postgresql://user:pass@localhost:5432/brazilretail_bi \
  python -m db_schema.create_schema

DATABASE_URL=... python -m db_schema.setup_constraints
```

Supabase tables are managed in the dashboard SQL editor; `db_schema/migration_to_supabase.py` exports CSV + SQL artifacts if you want to migrate from local.
