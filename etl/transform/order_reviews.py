from __future__ import annotations

import pandas as pd

from .common import finalize, nat_to_none, strip_timezone


def transform_order_reviews(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    for col in ("review_id", "order_id", "review_comment_title", "review_comment_message"):
        data[col] = data[col].astype("string")
    data["review_score"] = data["review_score"].astype("Int64")

    data["review_creation_date"] = strip_timezone(data["review_creation_date"])
    data["review_answer_timestamp"] = strip_timezone(data["review_answer_timestamp"])

    data = finalize(data)
    # review_id is a soft key; the table PK is order_id, so one review per order.
    return data.drop_duplicates(subset=["review_id"], keep="first")
