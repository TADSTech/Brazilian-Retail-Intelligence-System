from sqlalchemy.orm import sessionmaker
from create_schema import engine, Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Product, Seller
from ..etl.utils import error_message, success_message

# Create session
Session = sessionmaker(bind=engine)

def load_customers(df):
    """Load customers data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(Customer, records)
        session.commit()
        success_message(f"Loaded {len(records)} customer records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load customers: {e}")
    finally:
        session.close()

def load_geolocation(df):
    """Load geolocation data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(Geolocation, records)
        session.commit()
        success_message(f"Loaded {len(records)} geolocation records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load geolocation: {e}")
    finally:
        session.close()

def load_order_items(df):
    """Load order items data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderItem, records)
        session.commit()
        success_message(f"Loaded {len(records)} order item records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order items: {e}")
    finally:
        session.close()

def load_order_payments(df):
    """Load order payments data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderPayment, records)
        session.commit()
        success_message(f"Loaded {len(records)} order payment records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order payments: {e}")
    finally:
        session.close()

def load_order_reviews(df):
    """Load order reviews data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(OrderReview, records)
        session.commit()
        success_message(f"Loaded {len(records)} order review records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load order reviews: {e}")
    finally:
        session.close()

def load_orders(df):
    """Load orders data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(Order, records)
        session.commit()
        success_message(f"Loaded {len(records)} order records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load orders: {e}")
    finally:
        session.close()

def load_products(df):
    """Load products data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(Product, records)
        session.commit()
        success_message(f"Loaded {len(records)} product records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load products: {e}")
    finally:
        session.close()

def load_sellers(df):
    """Load sellers data into the database."""
    try:
        session = Session()
        records = df.to_dict('records')
        session.bulk_insert_mappings(Seller, records)
        session.commit()
        success_message(f"Loaded {len(records)} seller records.")
    except Exception as e:
        session.rollback()
        error_message(f"Failed to load sellers: {e}")
    finally:
        session.close()