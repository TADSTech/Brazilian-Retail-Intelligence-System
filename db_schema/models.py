"""SQLAlchemy models for the local PostgreSQL schema."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base

from etl.config import settings

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    customer_unique_id = Column(String)
    customer_zip_code_prefix = Column(String)
    customer_city = Column(String)
    customer_state = Column(String)
    customer_state_initials = Column(String)


class Geolocation(Base):
    __tablename__ = "geolocation"

    geolocation_id = Column(Integer, primary_key=True, autoincrement=True)
    geolocation_zip_code_prefix = Column(Integer)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)
    geolocation_state_initials = Column(String)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    order_purchase_timestamp = Column(DateTime)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(DateTime)


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(String, primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=False)
    seller_id = Column(String, nullable=False)
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)


class OrderPayment(Base):
    __tablename__ = "order_payments"

    order_id = Column(String, primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String, nullable=False)
    payment_installments = Column(Integer, nullable=False)
    payment_value = Column(Float, nullable=False)


class OrderReview(Base):
    __tablename__ = "order_reviews"

    review_id = Column(String)
    order_id = Column(String, primary_key=True)
    review_score = Column(Integer)
    review_comment_title = Column(Text)
    review_comment_message = Column(Text)
    review_creation_date = Column(DateTime)
    review_answer_timestamp = Column(DateTime)


class Product(Base):
    __tablename__ = "products"

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
    __tablename__ = "sellers"

    seller_id = Column(String, primary_key=True)
    seller_zip_code_prefix = Column(Integer)
    seller_city = Column(String)
    seller_state = Column(String)
    seller_state_initials = Column(String)


MODELS: dict[str, type[Base]] = {
    "customers": Customer,
    "geolocation": Geolocation,
    "orders": Order,
    "order_items": OrderItem,
    "order_payments": OrderPayment,
    "order_reviews": OrderReview,
    "products": Product,
    "sellers": Seller,
}


def get_engine(echo: bool = False):
    return create_engine(settings.require_postgres(), echo=echo)


# Shared engine used by the local loader and schema tooling.
engine = get_engine()
