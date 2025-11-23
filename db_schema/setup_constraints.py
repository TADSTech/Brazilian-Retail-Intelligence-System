import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not set.")
    exit(1)

def add_foreign_keys(connection):
    print("Adding foreign keys...")
    
    fks = [
        {
            "table": "orders",
            "constraint": "fk_orders_customers",
            "sql": "ALTER TABLE orders ADD CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers (customer_id);"
        },
        {
            "table": "order_items",
            "constraint": "fk_order_items_orders",
            "sql": "ALTER TABLE order_items ADD CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);"
        },
        {
            "table": "order_items",
            "constraint": "fk_order_items_products",
            "sql": "ALTER TABLE order_items ADD CONSTRAINT fk_order_items_products FOREIGN KEY (product_id) REFERENCES products (product_id);"
        },
        {
            "table": "order_items",
            "constraint": "fk_order_items_sellers",
            "sql": "ALTER TABLE order_items ADD CONSTRAINT fk_order_items_sellers FOREIGN KEY (seller_id) REFERENCES sellers (seller_id);"
        },
        {
            "table": "order_payments",
            "constraint": "fk_order_payments_orders",
            "sql": "ALTER TABLE order_payments ADD CONSTRAINT fk_order_payments_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);"
        },
        {
            "table": "order_reviews",
            "constraint": "fk_order_reviews_orders",
            "sql": "ALTER TABLE order_reviews ADD CONSTRAINT fk_order_reviews_orders FOREIGN KEY (order_id) REFERENCES orders (order_id);"
        }
    ]

    for fk in fks:
        try:
            # Check if constraint exists
            # This query is specific to Postgres
            check_sql = text(f"SELECT 1 FROM pg_constraint WHERE conname = '{fk['constraint']}'")
            result = connection.execute(check_sql).fetchone()
            
            if result:
                print(f"Constraint {fk['constraint']} already exists. Skipping.")
            else:
                connection.execute(text(fk['sql']))
                print(f"Added {fk['constraint']}")
        except Exception as e:
            print(f"Error adding {fk['constraint']}: {e}")

def add_indexes(connection):
    print("Adding indexes...")
    
    indexes = [
        # Foreign Key Indexes for performance
        {"name": "idx_orders_customer_id", "table": "orders", "column": "customer_id"},
        {"name": "idx_order_items_order_id", "table": "order_items", "column": "order_id"},
        {"name": "idx_order_items_product_id", "table": "order_items", "column": "product_id"},
        {"name": "idx_order_items_seller_id", "table": "order_items", "column": "seller_id"},
        {"name": "idx_order_payments_order_id", "table": "order_payments", "column": "order_id"},
        {"name": "idx_order_reviews_order_id", "table": "order_reviews", "column": "order_id"},
        
        # Other useful indexes based on common queries
        {"name": "idx_orders_status", "table": "orders", "column": "order_status"},
        {"name": "idx_orders_purchase_timestamp", "table": "orders", "column": "order_purchase_timestamp"},
        {"name": "idx_products_category", "table": "products", "column": "product_category_name"}
    ]

    for idx in indexes:
        try:
            # Check if index exists
            check_sql = text(f"SELECT 1 FROM pg_indexes WHERE indexname = '{idx['name']}'")
            result = connection.execute(check_sql).fetchone()
            
            if result:
                print(f"Index {idx['name']} already exists. Skipping.")
            else:
                create_sql = text(f"CREATE INDEX {idx['name']} ON {idx['table']} ({idx['column']})")
                connection.execute(create_sql)
                print(f"Added index {idx['name']}")
        except Exception as e:
            print(f"Error adding index {idx['name']}: {e}")

def main():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Start transaction
        trans = connection.begin()
        try:
            add_foreign_keys(connection)
            add_indexes(connection)
            trans.commit()
            print("Database constraints and indexes setup completed successfully.")
        except Exception as e:
            trans.rollback()
            print(f"Error during setup: {e}")
            raise e

if __name__ == "__main__":
    main()
