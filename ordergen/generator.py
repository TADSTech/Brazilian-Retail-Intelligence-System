import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from .utils import SimpleMarkovChain

class OrderGenerator:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.fake = Faker('pt_BR')  # Brazilian Portuguese locale
        self.markov = SimpleMarkovChain()
        
        # Learned distributions/lists
        self.product_ids = []
        self.seller_ids = []
        self.zip_codes = []
        self.cities = []
        self.states = []
        self.product_prices = {} # product_id -> list of prices
        
    def train(self):
        """
        Load existing data and learn distributions.
        """
        print("Training Order Generator...")
        
        # Load Products
        try:
            products_df = pd.read_csv(f"{self.data_dir}/olist_products_dataset.csv")
            self.product_ids = products_df['product_id'].dropna().tolist()
        except Exception as e:
            print(f"Warning: Could not load products: {e}")

        # Load Sellers
        try:
            sellers_df = pd.read_csv(f"{self.data_dir}/olist_sellers_dataset.csv")
            self.seller_ids = sellers_df['seller_id'].dropna().tolist()
        except Exception as e:
            print(f"Warning: Could not load sellers: {e}")

        # Load Geolocation (for realistic locations)
        try:
            geo_df = pd.read_csv(f"{self.data_dir}/olist_geolocation_dataset.csv")
            # Sample to save memory
            sample_geo = geo_df.sample(n=min(10000, len(geo_df)))
            self.zip_codes = sample_geo['geolocation_zip_code_prefix'].tolist()
            self.cities = sample_geo['geolocation_city'].tolist()
            self.states = sample_geo['geolocation_state'].tolist()
        except Exception as e:
            print(f"Warning: Could not load geolocation: {e}")

        # Load Order Items (for pricing)
        try:
            items_df = pd.read_csv(f"{self.data_dir}/olist_order_items_dataset.csv")
            # Create a map of product_id -> prices
            # Group by product_id and get unique prices to save memory
            price_map = items_df.groupby('product_id')['price'].apply(list).to_dict()
            self.product_prices = price_map
        except Exception as e:
            print(f"Warning: Could not load order items: {e}")

        # Load Reviews (for NLP)
        try:
            reviews_df = pd.read_csv(f"{self.data_dir}/olist_order_reviews_dataset.csv")
            comments = reviews_df['review_comment_message'].dropna().astype(str).tolist()
            # Train on a subset to be fast
            self.markov.train(comments[:5000])
        except Exception as e:
            print(f"Warning: Could not load reviews: {e}")
            
        print("Training complete.")

    def generate_orders(self, num_orders=10, start_date=None, end_date=None):
        """
        Generate synthetic data.
        Returns a dictionary of DataFrames.
        """
        print(f"Generating {num_orders} orders...")
        
        orders = []
        customers = []
        order_items = []
        order_payments = []
        order_reviews = []
        
        for _ in range(num_orders):
            # 1. Generate Customer
            customer_id = str(uuid.uuid4())
            customer_unique_id = str(uuid.uuid4())
            
            # Pick a random location from learned data or fake it
            if self.zip_codes:
                idx = random.randint(0, len(self.zip_codes) - 1)
                zip_code = self.zip_codes[idx]
                city = self.cities[idx]
                state = self.states[idx]
            else:
                zip_code = self.fake.postcode()
                city = self.fake.city()
                state = self.fake.state_abbr()
                
            customers.append({
                'customer_id': customer_id,
                'customer_unique_id': customer_unique_id,
                'customer_zip_code_prefix': zip_code,
                'customer_city': city,
                'customer_state': state
            })
            
            # 2. Generate Order
            order_id = str(uuid.uuid4())
            
            # Date generation logic
            if start_date and end_date:
                time_between = end_date - start_date
                days_between = time_between.days
                random_days = random.randint(0, days_between)
                purchase_timestamp = start_date + timedelta(days=random_days, minutes=random.randint(0, 1440))
            else:
                # Default: Random date within last 30 days
                purchase_timestamp = datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440))
                
            approved_at = purchase_timestamp + timedelta(minutes=random.randint(10, 600))
            delivered_carrier = approved_at + timedelta(days=random.randint(1, 3))
            delivered_customer = delivered_carrier + timedelta(days=random.randint(1, 10))
            estimated_delivery = purchase_timestamp + timedelta(days=random.randint(10, 20))
            
            orders.append({
                'order_id': order_id,
                'customer_id': customer_id,
                'order_status': 'delivered', # Simplify to delivered for now
                'order_purchase_timestamp': purchase_timestamp,
                'order_approved_at': approved_at,
                'order_delivered_carrier_date': delivered_carrier,
                'order_delivered_customer_date': delivered_customer,
                'order_estimated_delivery_date': estimated_delivery
            })
            
            # 3. Generate Order Items
            num_items = random.randint(1, 3)
            total_value = 0
            
            for i in range(num_items):
                if self.product_ids:
                    product_id = random.choice(self.product_ids)
                else:
                    product_id = str(uuid.uuid4()) # Fallback
                    
                if self.seller_ids:
                    seller_id = random.choice(self.seller_ids)
                else:
                    seller_id = str(uuid.uuid4())
                
                # Get price
                price = 50.0
                if product_id in self.product_prices:
                    price = random.choice(self.product_prices[product_id])
                
                freight = random.uniform(10, 50)
                total_value += price + freight
                
                order_items.append({
                    'order_id': order_id,
                    'order_item_id': i + 1,
                    'product_id': product_id,
                    'seller_id': seller_id,
                    'shipping_limit_date': approved_at + timedelta(days=3),
                    'price': price,
                    'freight_value': freight
                })
                
            # 4. Generate Payments
            order_payments.append({
                'order_id': order_id,
                'payment_sequential': 1,
                'payment_type': random.choice(['credit_card', 'boleto', 'voucher', 'debit_card']),
                'payment_installments': random.randint(1, 10),
                'payment_value': total_value
            })
            
            # 5. Generate Reviews (70% chance)
            if random.random() < 0.7:
                review_id = str(uuid.uuid4())
                score = random.choices([5, 4, 3, 2, 1], weights=[0.5, 0.2, 0.1, 0.1, 0.1])[0]
                
                title = None
                message = None
                if random.random() < 0.4:
                    title = self.fake.sentence(nb_words=3)
                if random.random() < 0.6:
                    message = self.markov.generate(max_words=20)
                    
                order_reviews.append({
                    'review_id': review_id,
                    'order_id': order_id,
                    'review_score': score,
                    'review_comment_title': title,
                    'review_comment_message': message,
                    'review_creation_date': delivered_customer + timedelta(days=1),
                    'review_answer_timestamp': delivered_customer + timedelta(days=2)
                })

        return {
            'orders': pd.DataFrame(orders),
            'customers': pd.DataFrame(customers),
            'order_items': pd.DataFrame(order_items),
            'order_payments': pd.DataFrame(order_payments),
            'order_reviews': pd.DataFrame(order_reviews)
        }
