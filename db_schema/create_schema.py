from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/brazilretail_bi')

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for models
Base = declarative_base()

# Customers table model
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String, nullable=True)
    customer_unique_id = Column(String, primary_key=True)
    customer_zip_code_prefix = Column(String)
    customer_city = Column(String)
    customer_state = Column(String)
    customer_state_initials = Column(String)

class Geolocation(Base):
    __tablename__ = 'geolocation'

    geolocation_zip_code_prefix = Column(Integer, primary_key=True)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)
    geolocation_state_initials = Column(String)

class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    seller_id = Column(String, nullable=False)
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)

# Create all tables
def create_database_schema():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(engine)
        print("Database schema created successfully.")
    except Exception as e:
        print(f"Error creating database schema: {e}")
        print("Tables may already exist or there may be a database connection issue.")

if __name__ == "__main__":
    create_database_schema()