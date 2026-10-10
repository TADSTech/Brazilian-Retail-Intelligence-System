from __future__ import annotations

import pandas as pd

from .common import finalize, map_state_initials


def transform_geolocation(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["geolocation_zip_code_prefix"] = data["geolocation_zip_code_prefix"].astype("Int64")
    data["geolocation_lat"] = data["geolocation_lat"].astype("float64")
    data["geolocation_lng"] = data["geolocation_lng"].astype("float64")
    data["geolocation_city"] = data["geolocation_city"].astype("string").str.title()
    data["geolocation_state"] = data["geolocation_state"].astype("string")

    data["geolocation_state_initials"] = data["geolocation_state"]
    data["geolocation_state"] = map_state_initials(data["geolocation_state"])
    data = finalize(data)

    # The source CSV has no id column; the DB table uses a SERIAL primary key.
    # Assign a deterministic id (stable sort, then 1..N) so re-runs upsert on the
    # PK instead of blind-inserting duplicate rows.
    data = data.sort_values(by=list(data.columns), kind="mergesort").reset_index(drop=True)
    data["geolocation_id"] = range(1, len(data) + 1)
    return data
