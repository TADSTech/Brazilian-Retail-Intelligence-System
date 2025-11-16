from ..db_schema.dbmanip import (
    load_customers, load_geolocation, load_order_items, load_order_payments,
    load_order_reviews, load_orders, load_products, load_sellers
)

def load_all_data(transformed_data):
    """
    Load all transformed datasets into the database.
    
    Arguments:
        transformed_data (dict): Dictionary containing all transformed DataFrames
    """
    load_customers(transformed_data['customers'])
    load_geolocation(transformed_data['geolocation'])
    load_order_items(transformed_data['order_items'])
    load_order_payments(transformed_data['order_payments'])
    load_order_reviews(transformed_data['order_reviews'])
    load_orders(transformed_data['orders'])
    load_products(transformed_data['products'])
    load_sellers(transformed_data['sellers'])