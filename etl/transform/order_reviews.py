from __future__ import annotations

import pandas as pd

from .common import strip_timezone


def transform_order_reviews(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    for col in ("review_id", "order_id", "review_comment_title", "review_comment_message"):
        data[col] = data[col].astype("string")
    data["review_score"] = data["review_score"].astype("Int64")

    data["review_creation_date"] = strip_timezone(data["review_creation_date"])
    data["review_answer_timestamp"] = strip_timezone(data["review_answer_timestamp"])

    # Deliberately NOT finalize(): 56k+ reviews have a score but no free-text
    # title/message, and finalize's dropna would discard them. Text columns
    # are nullable in the schema. Soft-dedupe on review_id, then enforce the
    # table PK (one row per order_id — 551 raw orders have multiple reviews).
    data = data.dropna(subset=["order_id"])
    data = data.drop_duplicates(subset=["review_id"], keep="first")
    return data.drop_duplicates(subset=["order_id"], keep="first")
