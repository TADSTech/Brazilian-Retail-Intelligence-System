"""Synthetic order generation trained on live table distributions."""

from __future__ import annotations

import logging
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

from etl.config import settings
from etl.loaders import SupabaseLoader

from .markov import SimpleMarkovChain

logger = logging.getLogger(__name__)


class OrderGenerator:
    """Generates referentially consistent synthetic orders.

    Products, sellers, and locations are sampled from the database so foreign
    keys resolve. Prices are sampled from observed product prices when
    available. Review text comes from a Markov model trained on real comments
    (requires the source CSVs) or falls back to empty bodies.
    """

    def __init__(self, data_dir: str | Path | None = None):
        self.fake = Faker("pt_BR")
        self.markov = SimpleMarkovChain()
        self.data_dir = Path(data_dir) if data_dir else settings.data_dir
        self.loader = SupabaseLoader()
        self.client = self.loader.client

        self.product_ids: list[str] = []
        self.seller_ids: list[str] = []
        self.zip_codes: list[int] = []
        self.cities: list[str] = []
        self.states: list[str] = []
        self.product_prices: dict[str, list[float]] = {}

    def train(self) -> None:
        """Learn ID pools, prices, and locations from Supabase (+ CSVs if present)."""
        logger.info("Training order generator from database")

        self.product_ids = self._select_column("products", "product_id")
        self.seller_ids = self._select_column("sellers", "seller_id")

        try:
            response = (
                self.client.table("geolocation")
                .select("geolocation_zip_code_prefix,geolocation_city,geolocation_state")
                .limit(10000)
                .execute()
            )
            rows = response.data or []
            self.zip_codes = [r["geolocation_zip_code_prefix"] for r in rows]
            self.cities = [r["geolocation_city"] for r in rows]
            self.states = [r["geolocation_state"] for r in rows]
        except Exception:
            logger.exception("Could not load geolocation samples")

        self._train_prices_from_db()
        self._train_markov_from_csv()
        logger.info(
            "Training complete (products=%d sellers=%d locations=%d priced=%d)",
            len(self.product_ids),
            len(self.seller_ids),
            len(self.zip_codes),
            len(self.product_prices),
        )

    def _select_column(self, table: str, column: str) -> list[str]:
        try:
            response = self.client.table(table).select(column).execute()
            return [row[column] for row in (response.data or [])]
        except Exception:
            logger.exception("Could not load %s.%s", table, column)
            return []

    def _train_prices_from_db(self) -> None:
        try:
            response = (
                self.client.table("order_items")
                .select("product_id,price")
                .limit(50000)
                .execute()
            )
            for row in response.data or []:
                self.product_prices.setdefault(row["product_id"], []).append(row["price"])
        except Exception:
            logger.exception("Could not load historical prices from order_items")

    def _train_markov_from_csv(self) -> None:
        reviews_path = self.data_dir / "olist_order_reviews_dataset.csv"
        if not reviews_path.exists():
            logger.warning("Reviews CSV not found at %s; review bodies will be empty", reviews_path)
            return
        try:
            reviews = pd.read_csv(reviews_path)
            comments = reviews["review_comment_message"].dropna().astype(str).tolist()
            self.markov.train(comments[:5000])
        except Exception:
            logger.exception("Could not train Markov model from %s", reviews_path)

    def generate_orders(
        self,
        num_orders: int = 10,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Generate synthetic rows for the five order-family tables."""
        logger.info("Generating %d orders", num_orders)
        orders, customers, items, payments, reviews = [], [], [], [], []

        for _ in range(num_orders):
            customer_id, customer = self._make_customer()
            customers.append(customer)

            order_id, approved_at, order = self._make_order(customer_id, start_date, end_date)
            orders.append(order)

            total_value = 0.0
            for item_id in range(1, random.randint(1, 3) + 1):
                item, line_total = self._make_item(order_id, item_id, approved_at)
                items.append(item)
                total_value += line_total

            payments.append(
                {
                    "order_id": order_id,
                    "payment_sequential": 1,
                    "payment_type": random.choice(
                        ["credit_card", "boleto", "voucher", "debit_card"]
                    ),
                    "payment_installments": random.randint(1, 10),
                    "payment_value": total_value,
                }
            )

            if random.random() < 0.7:
                reviews.append(self._make_review(order_id, order["order_delivered_customer_date"]))

        return {
            "orders": pd.DataFrame(orders),
            "customers": pd.DataFrame(customers),
            "order_items": pd.DataFrame(items),
            "order_payments": pd.DataFrame(payments),
            "order_reviews": pd.DataFrame(reviews),
        }

    def _make_customer(self) -> tuple[str, dict]:
        customer_id = str(uuid.uuid4())
        if self.zip_codes:
            idx = random.randrange(len(self.zip_codes))
            zip_code, city, state = self.zip_codes[idx], self.cities[idx], self.states[idx]
        else:
            zip_code, city, state = (
                self.fake.postcode(),
                self.fake.city(),
                self.fake.state_abbr(),
            )
        return customer_id, {
            "customer_id": customer_id,
            "customer_unique_id": str(uuid.uuid4()),
            "customer_zip_code_prefix": zip_code,
            "customer_city": city,
            "customer_state": state,
        }

    def _make_order(
        self,
        customer_id: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> tuple[str, datetime, dict]:
        order_id = str(uuid.uuid4())
        if start_date and end_date:
            span = max((end_date - start_date).days, 0)
            purchase = start_date + timedelta(
                days=random.randint(0, span), minutes=random.randint(0, 1440)
            )
        else:
            purchase = datetime.now() - timedelta(
                days=random.randint(0, 30), minutes=random.randint(0, 1440)
            )
        approved = purchase + timedelta(minutes=random.randint(10, 600))
        carrier = approved + timedelta(days=random.randint(1, 3))
        delivered = carrier + timedelta(days=random.randint(1, 10))
        estimated = purchase + timedelta(days=random.randint(10, 20))
        return order_id, approved, {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_status": "delivered",
            "order_purchase_timestamp": purchase,
            "order_approved_at": approved,
            "order_delivered_carrier_date": carrier,
            "order_delivered_customer_date": delivered,
            "order_estimated_delivery_date": estimated,
        }

    def _make_item(
        self, order_id: str, item_id: int, approved_at: datetime
    ) -> tuple[dict, float]:
        product_id = random.choice(self.product_ids) if self.product_ids else str(uuid.uuid4())
        seller_id = random.choice(self.seller_ids) if self.seller_ids else str(uuid.uuid4())
        observed = self.product_prices.get(product_id)
        price = random.choice(observed) if observed else 50.0
        freight = random.uniform(10, 50)
        return {
            "order_id": order_id,
            "order_item_id": item_id,
            "product_id": product_id,
            "seller_id": seller_id,
            "shipping_limit_date": approved_at + timedelta(days=3),
            "price": price,
            "freight_value": freight,
        }, price + freight

    def _make_review(self, order_id: str, delivered) -> dict:
        body = self.markov.generate(max_words=20) if self.markov.start_words else None
        return {
            "review_id": str(uuid.uuid4()),
            "order_id": order_id,
            "review_score": random.choices([5, 4, 3, 2, 1], weights=[0.5, 0.2, 0.1, 0.1, 0.1])[0],
            "review_comment_title": self.fake.sentence(nb_words=3) if random.random() < 0.4 else None,
            "review_comment_message": body if random.random() < 0.6 else None,
            "review_creation_date": delivered + timedelta(days=1) if delivered else None,
            "review_answer_timestamp": delivered + timedelta(days=2) if delivered else None,
        }
