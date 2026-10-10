from __future__ import annotations

import pandas as pd

from .common import nat_to_none, strip_timezone


def transform_orders(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    for col in ("order_id", "customer_id", "order_status"):
        data[col] = data[col].astype("string")

    timestamp_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in timestamp_columns:
        if col in data.columns:
            data[col] = nat_to_none(strip_timezone(data[col]))

    # Deliberately NOT finalize(): non-delivered orders always lack both
    # delivery-date columns, and finalize's dropna would discard them
    # (breaking FKs from order_items/payments/reviews). All timestamp
    # columns are nullable in the schema.
    data = data.dropna(subset=["order_id", "customer_id", "order_status"])
    return data.drop_duplicates()
