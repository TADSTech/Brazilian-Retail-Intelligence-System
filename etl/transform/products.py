from __future__ import annotations

import pandas as pd

from .common import load_category_translations


def transform_products(
    data: pd.DataFrame, data_dir: str | None = None
) -> pd.DataFrame:
    data = data.copy()
    data["product_id"] = data["product_id"].astype("string")
    data["product_category_name"] = data["product_category_name"].astype("string")

    int_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in int_cols:
        if col in data.columns:
            data[col] = data[col].astype("Int64")

    translations = load_category_translations(data_dir) if data_dir else {}
    if translations:
        english = data["product_category_name"].map(translations)
        data["product_category_name_english"] = english.apply(
            lambda name: name.replace("_", " ").title() if isinstance(name, str) else name
        )
    else:
        data["product_category_name_english"] = data["product_category_name"]

    # Deliberately NOT finalize(): 611 products lack two or more dimension
    # columns and finalize would drop them, breaking fk_order_items_products.
    # Every column except product_id is nullable in the schema.
    data = data.dropna(subset=["product_id"])
    return data.drop_duplicates()
