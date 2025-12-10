import os
import sys
# The main imports
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from etl_prod.main import extract_and_transform, load_all_data, load_incremental
from ordergen.generator import OrderGenerator
from etl_prod.transform.customers import transform_customers
from etl_prod.transform.orders import transform_orders
from etl_prod.transform.orders_items import transform_order_items
from etl_prod.transform.order_payments import transform_order_payments
from etl_prod.transform.order_reviews import transform_order_reviews
from etl_prod.utils import log_message, success_message, error_message

app = FastAPI(title="Brazil Retail Intelligence API")

# Global Generator Instance
gen = None

@app.on_event("startup")
async def startup_event():
    global gen
    log_message("Initializing Order Generator...")
    try:
        gen = OrderGenerator()
        gen.train()
        success_message("Order Generator initialized and trained.")
    except Exception as e:
        error_message(f"Failed to initialize Order Generator: {e}")

class OrderGenRequest(BaseModel):
    count: int = 10

class ETLRequest(BaseModel):
    full_reload: bool = False
    tables: Optional[List[str]] = None

def run_etl_task(full_reload: bool, tables: Optional[List[str]]):
    log_message(f"Starting ETL Task. Full Reload: {full_reload}, Tables: {tables}")
    try:
        transformed_data = extract_and_transform()
        if full_reload:
            load_all_data(transformed_data)
        else:
            load_incremental(transformed_data, tables)
        success_message("ETL Task Completed Successfully.")
    except Exception as e:
        error_message(f"ETL Task Failed: {e}")

def run_order_gen_task(count: int):
    log_message(f"Starting Order Generation Task. Count: {count}")
    try:
        if not gen:
            raise Exception("Order Generator not initialized.")
            
        raw_data = gen.generate_orders(count)
        
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
            
        load_incremental(transformed_data)
        success_message(f"Generated and loaded {count} orders.")
    except Exception as e:
        error_message(f"Order Generation Task Failed: {e}")

@app.post("/etl/run")
async def trigger_etl(request: ETLRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_etl_task, request.full_reload, request.tables)
    return {"message": "ETL task started in background"}

@app.post("/orders/generate")
async def trigger_order_gen(request: OrderGenRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_order_gen_task, request.count)
    return {"message": f"Order generation task for {request.count} orders started in background"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
