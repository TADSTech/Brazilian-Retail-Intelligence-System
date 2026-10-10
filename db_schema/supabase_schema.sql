-- Schema for the Supabase backend (idempotent — safe to re-run).
-- Created from db_schema/models.py; FKs + indexes match db_schema/setup_constraints.py.
-- Run this in the Supabase SQL Editor (Dashboard -> SQL Editor -> New query).
-- No database password needed. After this, python -m etl loads via the service key alone.



CREATE TABLE IF NOT EXISTS geolocation (
	geolocation_id SERIAL NOT NULL, 
	geolocation_zip_code_prefix INTEGER, 
	geolocation_lat FLOAT, 
	geolocation_lng FLOAT, 
	geolocation_city VARCHAR, 
	geolocation_state VARCHAR, 
	geolocation_state_initials VARCHAR, 
	PRIMARY KEY (geolocation_id)
);

CREATE TABLE IF NOT EXISTS customers (
	customer_id VARCHAR NOT NULL, 
	customer_unique_id VARCHAR, 
	customer_zip_code_prefix VARCHAR, 
	customer_city VARCHAR, 
	customer_state VARCHAR, 
	customer_state_initials VARCHAR, 
	PRIMARY KEY (customer_id)
);

CREATE TABLE IF NOT EXISTS sellers (
	seller_id VARCHAR NOT NULL, 
	seller_zip_code_prefix INTEGER, 
	seller_city VARCHAR, 
	seller_state VARCHAR, 
	seller_state_initials VARCHAR, 
	PRIMARY KEY (seller_id)
);

CREATE TABLE IF NOT EXISTS products (
	product_id VARCHAR NOT NULL, 
	product_category_name VARCHAR, 
	product_category_name_english VARCHAR, 
	product_name_lenght INTEGER, 
	product_description_lenght INTEGER, 
	product_photos_qty INTEGER, 
	product_weight_g INTEGER, 
	product_length_cm INTEGER, 
	product_height_cm INTEGER, 
	product_width_cm INTEGER, 
	PRIMARY KEY (product_id)
);

CREATE TABLE IF NOT EXISTS orders (
	order_id VARCHAR NOT NULL, 
	customer_id VARCHAR NOT NULL, 
	order_status VARCHAR NOT NULL, 
	order_purchase_timestamp TIMESTAMP WITHOUT TIME ZONE, 
	order_approved_at TIMESTAMP WITHOUT TIME ZONE, 
	order_delivered_carrier_date TIMESTAMP WITHOUT TIME ZONE, 
	order_delivered_customer_date TIMESTAMP WITHOUT TIME ZONE, 
	order_estimated_delivery_date TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS order_items (
	order_id VARCHAR NOT NULL, 
	order_item_id INTEGER NOT NULL, 
	product_id VARCHAR NOT NULL, 
	seller_id VARCHAR NOT NULL, 
	shipping_limit_date TIMESTAMP WITHOUT TIME ZONE, 
	price FLOAT, 
	freight_value FLOAT, 
	PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS order_payments (
	order_id VARCHAR NOT NULL, 
	payment_sequential INTEGER NOT NULL, 
	payment_type VARCHAR NOT NULL, 
	payment_installments INTEGER NOT NULL, 
	payment_value FLOAT NOT NULL, 
	PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE IF NOT EXISTS order_reviews (
	review_id VARCHAR, 
	order_id VARCHAR NOT NULL, 
	review_score INTEGER, 
	review_comment_title TEXT, 
	review_comment_message TEXT, 
	review_creation_date TIMESTAMP WITHOUT TIME ZONE, 
	review_answer_timestamp TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (order_id)
);

-- Foreign keys (guarded, matches setup_constraints.py)

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_orders_customers') THEN
    ALTER TABLE orders ADD CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers (customer_id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_order_items_orders') THEN
    ALTER TABLE order_items ADD CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_order_items_products') THEN
    ALTER TABLE order_items ADD CONSTRAINT fk_order_items_products FOREIGN KEY (product_id) REFERENCES products (product_id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_order_items_sellers') THEN
    ALTER TABLE order_items ADD CONSTRAINT fk_order_items_sellers FOREIGN KEY (seller_id) REFERENCES sellers (seller_id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_order_payments_orders') THEN
    ALTER TABLE order_payments ADD CONSTRAINT fk_order_payments_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_order_reviews_orders') THEN
    ALTER TABLE order_reviews ADD CONSTRAINT fk_order_reviews_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);
  END IF;
END $$;

-- Indexes (guarded, matches setup_constraints.py)

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items (order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items (product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_seller_id ON order_items (seller_id);

CREATE INDEX IF NOT EXISTS idx_order_payments_order_id ON order_payments (order_id);

CREATE INDEX IF NOT EXISTS idx_order_reviews_order_id ON order_reviews (order_id);

CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (order_status);

CREATE INDEX IF NOT EXISTS idx_orders_purchase_timestamp ON orders (order_purchase_timestamp);

CREATE INDEX IF NOT EXISTS idx_products_category ON products (product_category_name);

CREATE INDEX IF NOT EXISTS idx_geolocation_zip_code_prefix ON geolocation (geolocation_zip_code_prefix);

-- Read access for the dashboard (anon) and logged-in clients

GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon, authenticated;
