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
    return finalize(data)
