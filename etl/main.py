from extract import extract_data
from transform.customers import transform_customers
from transform.geolocation import transform_geolocation
from transform.orders_items import transform_order_items
# from load import load_data
from utils import log_message, warning_message, error_message, success_message
import os

# Root directory of the project
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_etl_process():
    log_message("ETL process started.")
    
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
        transformed_geolocation = transformed_geolocation(geolocation_dataset)
        success_message("Geolocation data transformed successfully.")
        transformed_order_items = transform_order_items(order_items_dataset)
        success_message("Order items data transformed successfully.")
    except Exception as e:
        error_message(f"Data transformation failed: {e}")
        return
    log_message("Data transformation completed.")
    
    # # Load
    # load_data(transformed_data)
    # log_message("Data loading completed.")
    
    success_message("ETL process finished successfully.")

if __name__ == "__main__":
    run_etl_process()