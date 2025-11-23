import argparse
import os
import sys
from datetime import datetime
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
    parser = argparse.ArgumentParser(description="Backfill synthetic orders from 2018 to 2025.")
    parser.add_argument('--count', type=int, default=5000, help="Total number of orders to generate.")
    parser.add_argument('--data-dir', type=str, default=os.path.join(project_root, 'data'), help="Path to existing data for training.")
    
    args = parser.parse_args()
    
    # Define the gap period
    # Olist dataset ends roughly in Oct 2018
    start_date = datetime(2018, 10, 18)
    end_date = datetime.now()
    
    log_message(f"Starting backfill from {start_date.date()} to {end_date.date()}...")
    log_message(f"Target: {args.count} orders.")
    
    try:
        # 1. Initialize and Train Generator
        gen = OrderGenerator(args.data_dir)
        gen.train()
        
        # 2. Generate Data with Date Range
        # We'll generate in batches to avoid memory issues if count is huge
        batch_size = 1000
        total_generated = 0
        
        while total_generated < args.count:
            current_batch_size = min(batch_size, args.count - total_generated)
            log_message(f"Generating batch of {current_batch_size} orders...")
            
            raw_data = gen.generate_orders(
                num_orders=current_batch_size,
                start_date=start_date,
                end_date=end_date
            )
            
            # 3. Transform Data
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
            
            # 4. Load Data
            log_message("Loading batch into Supabase...")
            load_incremental(transformed_data)
            
            total_generated += current_batch_size
            success_message(f"Batch complete. Total progress: {total_generated}/{args.count}")
            
        success_message(f"Successfully backfilled {total_generated} orders.")
        
    except Exception as e:
        error_message(f"Backfill failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
