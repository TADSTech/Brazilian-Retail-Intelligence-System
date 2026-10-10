from __future__ import annotations

import pandas as pd

from .common import finalize, map_state_initials


def transform_customers(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    for col in ("customer_id", "customer_unique_id", "customer_city", "customer_state"):
        data[col] = data[col].astype("string")

    data["customer_city"] = data["customer_city"].str.title()
    data["customer_state_initials"] = data["customer_state"]
    data["customer_state"] = map_state_initials(data["customer_state"])
    return finalize(data)
