from .extract import extract_data
from .transform.customers import transform_customers
from .transform.geolocation import transform_geolocation
from .transform.orders_items import transform_order_items
from .transform.order_payments import transform_order_payments
from .transform.order_reviews import transform_order_reviews
from .transform.orders import transform_orders
from .transform.products import transform_products
from .transform.sellers import transform_sellers
from .load import load_all_data
from .utils import log_message, warning_message, error_message, success_message
import os
import sys

# Root directory of the project
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_etl_process(full_reload=False):
    """
    Run the complete ETL process.
    
    Args:
        full_reload (bool): If True, truncate existing data before loading. 
                           If False, skip if data already exists.
    """
    log_message("ETL process started.")
    
    # Check if schema exists
    from db_schema.create_schema import check_schema_created
    if not check_schema_created():
        error_message("Database schema not created. Please run 'python db_schema/create_schema.py' first.")
        return
    
    # Extract
    try:
        customer_dataset_path = os.path.join(root, "data/olist_customers_dataset.csv")
        customer_dataset = extract_data(customer_dataset_path)
        success_message("Customer data extracted successfully.")

        geolocation_dataset_path = os.path.join(root, "data/olist_geolocation_dataset.csv")
        geolocation_dataset = extract_data(geolocation_dataset_path)
        success_message("Geolocation data extracted successfully.")

        order_items_dataset_path = os.path.join(root, "data/olist_order_items_dataset.csv")
        order_items_dataset = extract_data(order_items_dataset_path)
        success_message("Order items data extracted successfully.")

        order_payments_dataset_path = os.path.join(root, "data/olist_order_payments_dataset.csv")
        order_payments_dataset = extract_data(order_payments_dataset_path)
        success_message("Order payments data extracted successfully.")

        order_reviews_dataset_path = os.path.join(root, "data/olist_order_reviews_dataset.csv")
        order_reviews_dataset = extract_data(order_reviews_dataset_path)
        success_message("Order reviews data extracted successfully.")

        orders_dataset_path = os.path.join(root, "data/olist_orders_dataset.csv")
        orders_dataset = extract_data(orders_dataset_path)
        success_message("Orders data extracted successfully.")

        products_dataset_path = os.path.join(root, "data/olist_products_dataset.csv")
        products_dataset = extract_data(products_dataset_path)
        success_message("Products data extracted successfully.")

        sellers_dataset_path = os.path.join(root, "data/olist_sellers_dataset.csv")
        sellers_dataset = extract_data(sellers_dataset_path)
        success_message("Sellers data extracted successfully.")

    except Exception as e:
        error_message(f"Data extraction failed: {e}")
        return
    log_message("Data extraction completed.")
    
    # Transform
    try:
        transformed_customers = transform_customers(customer_dataset)
        success_message("Customer data transformed successfully.")
        transformed_geolocation = transform_geolocation(geolocation_dataset)
        success_message("Geolocation data transformed successfully.")
        transformed_order_items = transform_order_items(order_items_dataset)
        success_message("Order items data transformed successfully.")
        transformed_order_payments = transform_order_payments(order_payments_dataset)
        success_message("Order payments data transformed successfully.")
        transformed_order_reviews = transform_order_reviews(order_reviews_dataset)
        success_message("Order reviews data transformed successfully.")
        transformed_orders = transform_orders(orders_dataset)
        success_message("Orders data transformed successfully.")
        transformed_products = transform_products(products_dataset)
        success_message("Products data transformed successfully.")
        transformed_sellers = transform_sellers(sellers_dataset)
        success_message("Sellers data transformed successfully.")
    except Exception as e:
        error_message(f"Data transformation failed: {e}")
        return
    log_message("Data transformation completed.")
    
    # Load
    try:
        transformed_data = {
            'customers': transformed_customers,
            'geolocation': transformed_geolocation,
            'order_items': transformed_order_items,
            'order_payments': transformed_order_payments,
            'order_reviews': transformed_order_reviews,
            'orders': transformed_orders,
            'products': transformed_products,
            'sellers': transformed_sellers,
            'full_reload': full_reload
        }
        load_all_data(transformed_data)
    except Exception as e:
        error_message(f"Data loading failed: {e}")
        return
    log_message("Data loading completed.")
    
    success_message("ETL process finished successfully.")

if __name__ == "__main__":
    full_reload = '--full-reload' in sys.argv
    run_etl_process(full_reload=full_reload)