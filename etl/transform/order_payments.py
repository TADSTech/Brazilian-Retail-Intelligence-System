from __future__ import annotations

import pandas as pd

from .common import finalize


def transform_order_payments(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["order_id"] = data["order_id"].astype("string")
    data["payment_sequential"] = data["payment_sequential"].astype("Int64")
    data["payment_type"] = data["payment_type"].astype("string")
    data["payment_installments"] = data["payment_installments"].astype("Int64")
    data["payment_value"] = data["payment_value"].astype("float64")
    return finalize(data)
