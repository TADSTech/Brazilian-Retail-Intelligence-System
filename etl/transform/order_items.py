from __future__ import annotations

import pandas as pd

from .common import finalize, strip_timezone


def transform_order_items(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    for col in ("order_id", "product_id", "seller_id"):
        data[col] = data[col].astype("string")

    data["shipping_limit_date"] = strip_timezone(data["shipping_limit_date"])
    return finalize(data)
