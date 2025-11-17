from ..db_schema.dbmanip import (
    load_customers, load_geolocation, load_order_items, load_order_payments,
    load_order_reviews, load_orders, load_products, load_sellers
)

def load_all_data(transformed_data):
    """
    Load all transformed datasets into the database.
    
    Arguments:
        transformed_data (dict): Dictionary containing all transformed DataFrames and options
    """
    full_reload = transformed_data.get('full_reload', False)
    
    load_customers(transformed_data['customers'], full_reload)
    load_geolocation(transformed_data['geolocation'], full_reload)
    load_order_items(transformed_data['order_items'], full_reload)
    load_order_payments(transformed_data['order_payments'], full_reload)
    load_order_reviews(transformed_data['order_reviews'], full_reload)
    load_orders(transformed_data['orders'], full_reload)
    load_products(transformed_data['products'], full_reload)
    load_sellers(transformed_data['sellers'], full_reload)