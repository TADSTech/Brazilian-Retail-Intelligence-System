import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .create_schema import engine, Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Product, Seller
from etl.utils import log_message, error_message, success_message
from .create_schema import check_schema_created

# Create session
Session = sessionmaker(bind=engine)

def load_customers(df, full_reload=False):
    """Load customers data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            # Truncate table for full reload
            session.execute(text("TRUNCATE TABLE customers RESTART IDENTITY CASCADE;"))
            success_message("Customers table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(Customer, records)
        session.commit()
        success_message(f"Loaded {len(records)} customer records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load customers: {e}")
    finally:
        session.close()

def load_geolocation(df, full_reload=False):
    """Load geolocation data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE geolocation RESTART IDENTITY CASCADE;"))
            success_message("Geolocation table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(Geolocation, records)
        session.commit()
        success_message(f"Loaded {len(records)} geolocation records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load geolocation: {e}")
    finally:
        session.close()

def load_order_items(df, full_reload=False):
    """Load order items data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE order_items RESTART IDENTITY CASCADE;"))
            success_message("Order items table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderItem, records)
        session.commit()
        success_message(f"Loaded {len(records)} order item records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order items: {e}")
    finally:
        session.close()

def load_order_payments(df, full_reload=False):
    """Load order payments data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE order_payments RESTART IDENTITY CASCADE;"))
            success_message("Order payments table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderPayment, records)
        session.commit()
        success_message(f"Loaded {len(records)} order payment records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order payments: {e}")
    finally:
        session.close()

def load_order_reviews(df, full_reload=False):
    """Load order reviews data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE order_reviews RESTART IDENTITY CASCADE;"))
            success_message("Order reviews table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderReview, records)
        session.commit()
        success_message(f"Loaded {len(records)} order review records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order reviews: {e}")
    finally:
        session.close()

def load_orders(df, full_reload=False):
    """Load orders data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE;"))
            success_message("Orders table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(Order, records)
        session.commit()
        success_message(f"Loaded {len(records)} order records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load orders: {e}")
    finally:
        session.close()

def load_products(df, full_reload=False):
    """Load products data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
            success_message("Products table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(Product, records)
        session.commit()
        success_message(f"Loaded {len(records)} product records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load products: {e}")
    finally:
        session.close()

def load_sellers(df, full_reload=False):
    """Load sellers data into the database."""
    if not check_schema_created():
        error_message("Database schema not created. Please run create_schema.py first.")
        return
    
    try:
        session = Session()
        
        if full_reload:
            session.execute(text("TRUNCATE TABLE sellers RESTART IDENTITY CASCADE;"))
            success_message("Sellers table truncated for full reload.")
        
        records = df.to_dict('records')
        session.bulk_insert_mappings(Seller, records)
        session.commit()
        success_message(f"Loaded {len(records)} seller records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load sellers: {e}")
    finally:
        session.close()