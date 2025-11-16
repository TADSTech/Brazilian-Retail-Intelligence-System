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

# Create all tables
def create_database_schema():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(engine)
        print("Database schema created successfully.")
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

if __name__ == "__main__":
    create_database_schema()