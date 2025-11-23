import os
import pandas as pd
from supabase import create_client
from .utils import log_message, error_message, success_message

def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPERKEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPERKEY must be set in environment variables.")
    return create_client(url, key)

def batch_upsert(table_name, df, batch_size=1000):
    supabase = get_supabase_client()
    
    # Pre-process DataFrame for JSON serialization
    # Convert datetime objects to ISO format strings
    df_clean = df.copy()
    for col in df_clean.columns:
        if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
            
    # Convert to records and handle NaN -> None for JSON compatibility
    records = df_clean.where(pd.notnull(df_clean), None).to_dict('records')
    total = len(records)
    
    log_message(f"Upserting {total} records into {table_name}...")
    
    for i in range(0, total, batch_size):
        batch = records[i:i+batch_size]
        try:
            supabase.table(table_name).upsert(batch).execute()
        except Exception as e:
            error_message(f"Failed to upsert batch to {table_name}: {e}")
            raise e
    success_message(f"Completed upsert for {table_name}")

def load_all_data(transformed_data):
    """
    Load all transformed datasets into Supabase.
    """
    # Mapping of data keys to Supabase table names
    # Order matters for Foreign Key constraints!
    tables = {
        'geolocation': 'geolocation',
        'customers': 'customers',
        'sellers': 'sellers',
        'products': 'products',
        'orders': 'orders',
        'order_items': 'order_items',
        'order_payments': 'order_payments',
        'order_reviews': 'order_reviews'
    }
    
    for key, table_name in tables.items():
        if key in transformed_data:
            df = transformed_data[key]
            if df is not None and not df.empty:
                batch_upsert(table_name, df)

def load_incremental(transformed_data, tables_to_update=None):
    """
    Load only specific tables or new data.
    Args:
        transformed_data (dict): Dictionary of DataFrames
        tables_to_update (list): List of keys to update (e.g. ['orders', 'order_items'])
    """
    # Order matters for Foreign Key constraints!
    tables = {
        'geolocation': 'geolocation',
        'customers': 'customers',
        'sellers': 'sellers',
        'products': 'products',
        'orders': 'orders',
        'order_items': 'order_items',
        'order_payments': 'order_payments',
        'order_reviews': 'order_reviews'
    }
    
    if tables_to_update is None:
        tables_to_update = list(tables.keys())
        
    # Ensure we process tables in the correct dependency order
    # Filter the ordered keys by what's requested
    ordered_update_keys = [k for k in tables.keys() if k in tables_to_update]
        
    for key in ordered_update_keys:
        if key in transformed_data and key in tables:
            df = transformed_data[key]
            if df is not None and not df.empty:
                log_message(f"Incremental update for {key}...")
                batch_upsert(tables[key], df)
