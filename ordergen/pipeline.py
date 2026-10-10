"""Shared transform+load step for generated order batches."""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd

from etl.loaders import Loader, get_loader
from etl.logging_config import configure_logging
from etl.transform import (
    transform_customers,
    transform_order_items,
    transform_order_payments,
    transform_order_reviews,
    transform_orders,
)

from .generator import OrderGenerator

logger = logging.getLogger(__name__)

_GENERATED_TRANSFORMS = {
    "customers": transform_customers,
    "orders": transform_orders,
    "order_items": transform_order_items,
    "order_payments": transform_order_payments,
    "order_reviews": transform_order_reviews,
}


def transform_generated(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Run the production transformers over generated frames (schema compliance)."""
    out: dict[str, pd.DataFrame] = {}
    for table, fn in _GENERATED_TRANSFORMS.items():
        df = raw.get(table)
        if df is not None and not df.empty:
            out[table] = fn(df)
    return out


def generate_and_load(
    gen: OrderGenerator,
    count: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    loader: Loader | None = None,
) -> dict[str, int]:
    raw = gen.generate_orders(count, start_date=start_date, end_date=end_date)
    transformed = transform_generated(raw)
    return (loader or get_loader()).load(transformed)


def build_generator(data_dir: str | None = None) -> OrderGenerator:
    configure_logging()
    gen = OrderGenerator(data_dir=data_dir)
    gen.train()
    return gen
