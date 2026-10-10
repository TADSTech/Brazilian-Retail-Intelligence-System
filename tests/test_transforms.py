from __future__ import annotations

import pandas as pd

from etl.transform import (
    STATE_NAMES,
    transform_customers,
    transform_order_reviews,
    transform_orders,
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
