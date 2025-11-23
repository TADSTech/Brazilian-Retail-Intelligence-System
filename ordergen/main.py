import argparse
import os
import sys
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ordergen.generator import OrderGenerator
from etl_prod.transform.customers import transform_customers
from etl_prod.transform.orders import transform_orders
from etl_prod.transform.orders_items import transform_order_items
from etl_prod.transform.order_payments import transform_order_payments
from etl_prod.transform.order_reviews import transform_order_reviews
from etl_prod.load import load_incremental
from etl_prod.utils import log_message, success_message, error_message

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic orders and load them into Supabase.")
    parser.add_argument('--count', type=int, default=10, help="Number of orders to generate.")
    parser.add_argument('--data-dir', type=str, default=os.path.join(project_root, 'data'), help="Path to existing data for training.")
    
    args = parser.parse_args()
    
    try:
        # 1. Initialize and Train Generator
        gen = OrderGenerator(args.data_dir)
        gen.train()
        
        # 2. Generate Data
        raw_data = gen.generate_orders(args.count)
        
        # 3. Transform Data
        # We reuse the production transformers to ensure data quality and schema compliance
        log_message("Transforming generated data...")
        transformed_data = {}
        
        if not raw_data['customers'].empty:
            transformed_data['customers'] = transform_customers(raw_data['customers'])
            
        if not raw_data['orders'].empty:
            transformed_data['orders'] = transform_orders(raw_data['orders'])
            
        if not raw_data['order_items'].empty:
            transformed_data['order_items'] = transform_order_items(raw_data['order_items'])
            
        if not raw_data['order_payments'].empty:
            transformed_data['order_payments'] = transform_order_payments(raw_data['order_payments'])
            
        if not raw_data['order_reviews'].empty:
            transformed_data['order_reviews'] = transform_order_reviews(raw_data['order_reviews'])
            
        # Note: We are not generating new products, sellers, or geolocation data in this version,
        # so we don't need to transform/load them. We reuse existing ones.
        
        success_message("Data transformation complete.")
        
        # 4. Load Data
        log_message("Loading data into Supabase...")
        # We use load_incremental to upsert the new records
        load_incremental(transformed_data)
        
        success_message(f"Successfully generated and loaded {args.count} orders.")
        
    except Exception as e:
        error_message(f"Order generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
