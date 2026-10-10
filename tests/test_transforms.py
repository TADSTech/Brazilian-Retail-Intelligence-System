from __future__ import annotations

import pandas as pd

from etl.transform import (
    STATE_NAMES,
    transform_customers,
    transform_geolocation,
    transform_order_reviews,
    transform_orders,
    transform_products,
    transform_sellers,
)


def test_state_names_cover_all_ufs():
    assert len(STATE_NAMES) == 27
    assert STATE_NAMES["SP"] == "São Paulo"


def test_transform_customers_maps_state_and_keeps_initials():
    raw = pd.DataFrame(
        {
            "customer_id": ["c1", "c1"],
            "customer_unique_id": ["u1", "u1"],
            "customer_zip_code_prefix": [13000, 13000],
            "customer_city": ["são paulo", "são paulo"],
            "customer_state": ["SP", "SP"],
        }
    )
    out = transform_customers(raw)
    assert len(out) == 1
    assert out.iloc[0]["customer_state"] == "São Paulo"
    assert out.iloc[0]["customer_state_initials"] == "SP"
    assert out.iloc[0]["customer_city"] == "São Paulo"


def test_transform_sellers_maps_state():
    raw = pd.DataFrame(
        {
            "seller_id": ["s1"],
            "seller_zip_code_prefix": [13000],
            "seller_city": ["rio de janeiro"],
            "seller_state": ["RJ"],
        }
    )
    out = transform_sellers(raw)
    assert out.iloc[0]["seller_state"] == "Rio de Janeiro"
    assert out.iloc[0]["seller_state_initials"] == "RJ"


def test_transform_orders_strips_timezone_and_nat():
    raw = pd.DataFrame(
        {
            "order_id": ["o1"],
            "customer_id": ["c1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2018-01-01T10:00:00"],
            "order_approved_at": [None],
            "order_delivered_carrier_date": ["2018-01-02T10:00:00"],
            "order_delivered_customer_date": ["2018-01-05T10:00:00"],
            "order_estimated_delivery_date": ["2018-01-10T10:00:00"],
        }
    )
    out = transform_orders(raw)
    assert pd.isna(out.iloc[0]["order_approved_at"]) or out.iloc[0]["order_approved_at"] is None
    ts = out.iloc[0]["order_purchase_timestamp"]
    assert getattr(ts, "tzinfo", None) is None


def test_transform_order_reviews_dedupes_review_id():
    raw = pd.DataFrame(
        {
            "review_id": ["r1", "r1", "r2"],
            "order_id": ["o1", "o1", "o2"],
            "review_score": [5, 5, 4],
            "review_comment_title": [None, None, None],
            "review_comment_message": ["ok", "ok", "bom"],
            "review_creation_date": ["2018-01-01", "2018-01-01", "2018-01-02"],
            "review_answer_timestamp": ["2018-01-02", "2018-01-02", "2018-01-03"],
        }
    )
    out = transform_order_reviews(raw)
    assert out["review_id"].is_unique
    assert len(out) == 2


def test_transform_order_reviews_keeps_textless_reviews_and_one_per_order():
    raw = pd.DataFrame(
        {
            "review_id": ["r1", "r2", "r3"],
            "order_id": ["o1", "o1", "o2"],
            "review_score": [5, 4, 3],
            "review_comment_title": [None, None, None],
            "review_comment_message": [None, None, None],
            "review_creation_date": ["2018-01-01", "2018-01-02", "2018-01-03"],
            "review_answer_timestamp": [None, None, None],
        }
    )
    out = transform_order_reviews(raw)
    # Score-only reviews survive (text columns are nullable), PK stays unique.
    assert len(out) == 2
    assert out["order_id"].is_unique
    assert set(out["order_id"]) == {"o1", "o2"}


def test_transform_orders_keeps_orders_without_delivery_dates():
    raw = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "customer_id": ["c1", "c2"],
            "order_status": ["delivered", "canceled"],
            "order_purchase_timestamp": ["2018-01-01T10:00:00", "2018-01-02T10:00:00"],
            "order_approved_at": ["2018-01-01T11:00:00", None],
            "order_delivered_carrier_date": ["2018-01-02T09:00:00", None],
            "order_delivered_customer_date": ["2018-01-05T09:00:00", None],
            "order_estimated_delivery_date": ["2018-01-10T09:00:00", "2018-01-15T09:00:00"],
        }
    )
    out = transform_orders(raw)
    # A canceled order missing BOTH delivery dates must not be dropped —
    # order_items/payments/reviews reference it (FK integrity).
    assert len(out) == 2
    assert out["order_id"].is_unique


def test_transform_products_keeps_products_missing_dimensions():
    raw = pd.DataFrame(
        {
            "product_id": ["p1", "p2"],
            "product_category_name": ["beleza", "presentes"],
            "product_name_lenght": [None, None],
            "product_description_lenght": [None, None],
            "product_photos_qty": [None, None],
            "product_weight_g": [None, None],
            "product_length_cm": [None, None],
            "product_height_cm": [None, None],
            "product_width_cm": [None, None],
        }
    )
    out = transform_products(raw, data_dir=None)
    # Products lacking multiple dimensions are still referenced by order_items.
    assert len(out) == 2
    assert out["product_id"].is_unique


def test_transform_geolocation_assigns_deterministic_ids():
    raw = pd.DataFrame(
        {
            "geolocation_zip_code_prefix": [13000, 13001, 13000],
            "geolocation_lat": [-23.5, -23.6, -23.5],
            "geolocation_lng": [-46.6, -46.7, -46.6],
            "geolocation_city": ["sao paulo", "sao paulo", "sao paulo"],
            "geolocation_state": ["SP", "SP", "SP"],
        }
    )
    out1 = transform_geolocation(raw)
    out2 = transform_geolocation(raw)
    assert "geolocation_id" in out1.columns
    assert out1["geolocation_id"].is_unique
    # Same input -> same ids (idempotent upserts across runs).
    pd.testing.assert_frame_equal(out1, out2)
    # Row order in the source must not change the assigned ids.
    out3 = transform_geolocation(raw.sample(frac=1.0, random_state=7).reset_index(drop=True))
    assert list(out1["geolocation_id"]) == list(out3["geolocation_id"])
    assert list(out1["geolocation_zip_code_prefix"]) == list(out3["geolocation_zip_code_prefix"])
