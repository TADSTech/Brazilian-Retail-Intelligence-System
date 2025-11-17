from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://tads:TadsDB25@localhost:5432/brazilretail_bi')

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for models
Base = declarative_base()

# Customers table model
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String, primary_key=True)
    customer_unique_id = Column(String, nullable=True)
    customer_zip_code_prefix = Column(String)
    customer_city = Column(String)
    customer_state = Column(String)
    customer_state_initials = Column(String)

class Geolocation(Base):
    __tablename__ = 'geolocation'

    geolocation_id = Column(Integer, primary_key=True, autoincrement=True)
    geolocation_zip_code_prefix = Column(Integer)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)
    geolocation_state_initials = Column(String)

class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id = Column(String, primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=False)
    seller_id = Column(String, nullable=False)
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)

class OrderPayment(Base):
    __tablename__ = 'order_payments'

    order_id = Column(String, primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String, nullable=False)
    payment_installments = Column(Integer, nullable=False)
    payment_value = Column(Float, nullable=False)

class OrderReview(Base):
    __tablename__ = 'order_reviews'

    review_id = Column(String)
    order_id = Column(String, primary_key=True)
    review_score = Column(Integer)
    review_comment_title = Column(Text)
    review_comment_message = Column(Text)
    review_creation_date = Column(DateTime)
    review_answer_timestamp = Column(DateTime)

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    order_purchase_timestamp = Column(DateTime)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(DateTime)

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(String, primary_key=True)
    product_category_name = Column(String)
    product_category_name_english = Column(String)
    product_name_lenght = Column(Integer)
    product_description_lenght = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Integer)
    product_length_cm = Column(Integer)
    product_height_cm = Column(Integer)
    product_width_cm = Column(Integer)

class Seller(Base):
    __tablename__ = 'sellers'

    seller_id = Column(String, primary_key=True)
    seller_zip_code_prefix = Column(Integer)
    seller_city = Column(String)
    seller_state = Column(String)
    seller_state_initials = Column(String)

# Create all tables
def create_database_schema():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(engine)
        print("Database schema created successfully.")
        
        # Save flag file to indicate schema creation
        flag_file = os.path.join(os.path.dirname(__file__), '..', '.schema_created')
        with open(flag_file, 'w') as f:
            f.write('true')
        print("Schema creation flag saved.")
        
    except Exception as e:
        print(f"Error creating database schema: {e}")
        print("Tables may already exist or there may be a database connection issue.")

# Create customers table specifically
def create_customers_table():
    """Create the customers table."""
    try:
        Customer.__table__.create(engine)
        print("Customers table created successfully.")
    except Exception as e:
        print(f"Error creating customers table: {e}")
        print("Table may already exist or there may be a database connection issue.")

def check_schema_created():
    """Check if the database schema has been created."""
    flag_file = os.path.join(os.path.dirname(__file__), '..', '.schema_created')
    return os.path.exists(flag_file)

if __name__ == "__main__":
    create_database_schema()