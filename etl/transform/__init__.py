"""Pure transform functions, one module per table.

Every transform takes a raw DataFrame and returns a cleaned DataFrame.
`finalize` applies the shared row-quality rules (drop near-empty rows, dedupe).
"""

from __future__ import annotations

import logging

import pandas as pd

from .common import STATE_NAMES, finalize, load_category_translations
from .customers import transform_customers
from .geolocation import transform_geolocation
from .order_items import transform_order_items
from .order_payments import transform_order_payments
from .order_reviews import transform_order_reviews
from .orders import transform_orders
from .products import transform_products
from .sellers import transform_sellers

logger = logging.getLogger(__name__)

TRANSFORMS = {
    "customers": transform_customers,
    "geolocation": transform_geolocation,
    "order_items": transform_order_items,
    "order_payments": transform_order_payments,
    "order_reviews": transform_order_reviews,
    "orders": transform_orders,
    "products": transform_products,
    "sellers": transform_sellers,
}

__all__ = [
    "TRANSFORMS",
    "STATE_NAMES",
    "finalize",
    "load_category_translations",
    "transform_customers",
    "transform_geolocation",
    "transform_order_items",
    "transform_order_payments",
    "transform_order_reviews",
    "transform_orders",
    "transform_products",
    "transform_sellers",
]
