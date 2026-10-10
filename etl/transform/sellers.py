from __future__ import annotations

import pandas as pd

from .common import finalize, map_state_initials


def transform_sellers(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["seller_id"] = data["seller_id"].astype("string")
    data["seller_zip_code_prefix"] = data["seller_zip_code_prefix"].astype("Int64")
    data["seller_city"] = data["seller_city"].astype("string").str.title()
    data["seller_state"] = data["seller_state"].astype("string")

    data["seller_state_initials"] = data["seller_state"]
    data["seller_state"] = map_state_initials(data["seller_state"])
    return finalize(data)
