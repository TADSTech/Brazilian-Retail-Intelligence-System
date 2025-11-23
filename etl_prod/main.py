from .extract import extract_data
from .transform.customers import transform_customers
from .transform.geolocation import transform_geolocation
from .transform.orders_items import transform_order_items
from .transform.order_payments import transform_order_payments
from .transform.order_reviews import transform_order_reviews
from .transform.orders import transform_orders
from .transform.products import transform_products
from .transform.sellers import transform_sellers
from .load import load_all_data, load_incremental
from .utils import log_message, warning_message, error_message, success_message
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Root directory of the project
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_and_transform():
    log_message("Starting Extract and Transform...")
    # Extract
    try:
        customer_dataset = extract_data(os.path.join(root, "data/olist_customers_dataset.csv"))
        geolocation_dataset = extract_data(os.path.join(root, "data/olist_geolocation_dataset.csv"))
        order_items_dataset = extract_data(os.path.join(root, "data/olist_order_items_dataset.csv"))
        order_payments_dataset = extract_data(os.path.join(root, "data/olist_order_payments_dataset.csv"))
        order_reviews_dataset = extract_data(os.path.join(root, "data/olist_order_reviews_dataset.csv"))
        orders_dataset = extract_data(os.path.join(root, "data/olist_orders_dataset.csv"))
        products_dataset = extract_data(os.path.join(root, "data/olist_products_dataset.csv"))
        sellers_dataset = extract_data(os.path.join(root, "data/olist_sellers_dataset.csv"))
        success_message("Data extraction completed.")
    except Exception as e:
        error_message(f"Data extraction failed: {e}")
        raise e

    # Transform
    try:
        transformed_data = {
            'customers': transform_customers(customer_dataset),
            'geolocation': transform_geolocation(geolocation_dataset),
            'order_items': transform_order_items(order_items_dataset),
            'order_payments': transform_order_payments(order_payments_dataset),
            'order_reviews': transform_order_reviews(order_reviews_dataset),
            'orders': transform_orders(orders_dataset),
            'products': transform_products(products_dataset),
            'sellers': transform_sellers(sellers_dataset)
        }
        success_message("Data transformation completed.")
        return transformed_data
    except Exception as e:
        error_message(f"Data transformation failed: {e}")
        raise e

def run_etl_process(full_reload=False):
    log_message("ETL process started.")
    try:
        data = extract_and_transform()
        data['full_reload'] = full_reload
        load_all_data(data)
        success_message("ETL process finished successfully.")
    except Exception as e:
        error_message(f"ETL process failed: {e}")

def run_incremental_etl(tables_to_update=None):
    log_message("Incremental ETL process started.")
    try:
        data = extract_and_transform()
        load_incremental(data, tables_to_update)
        success_message("Incremental ETL process finished successfully.")
    except Exception as e:
        error_message(f"Incremental ETL process failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ETL Process")
    parser.add_argument('--full-reload', action='store_true', help="Full reload of data")
    parser.add_argument('--incremental', action='store_true', help="Run incremental update")
    parser.add_argument('--tables', nargs='+', help="Specific tables to update incrementally")
    
    args = parser.parse_args()
    
    if args.incremental:
        run_incremental_etl(args.tables)
    else:
        run_etl_process(full_reload=args.full_reload)
