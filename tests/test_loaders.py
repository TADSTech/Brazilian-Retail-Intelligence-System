from __future__ import annotations

import pandas as pd

from etl.config import TABLE_ORDER
from etl.loaders import Loader, records_for_json


class FakeLoader(Loader):
    def __init__(self):
        self.calls: list[tuple[str, int]] = []

    def upsert(self, table: str, df: pd.DataFrame) -> int:
        self.calls.append((table, len(df)))
        return len(df)


def test_table_order_is_fk_safe():
    assert TABLE_ORDER[0] == "geolocation"
    assert TABLE_ORDER.index("orders") < TABLE_ORDER.index("order_items")
    assert TABLE_ORDER.index("customers") < TABLE_ORDER.index("orders")
    assert len(TABLE_ORDER) == 8


def test_loader_respects_fk_order_and_filter():
    loader = FakeLoader()
    data = {t: pd.DataFrame({"x": [1]}) for t in TABLE_ORDER}
    results = loader.load(data, tables=["orders", "order_items", "customers"])
    assert [c[0] for c in loader.calls] == ["customers", "orders", "order_items"]
    assert results["orders"] == 1


def test_records_for_json_converts_nat_and_timestamps():
    df = pd.DataFrame(
        {
            "ts": pd.to_datetime(["2018-01-01T00:00:00", None]),
            "n": [1.0, float("nan")],
        }
    )
    records = records_for_json(df)
    assert records[0]["ts"].startswith("2018-01-01")
    assert records[1]["ts"] is None
    assert records[1]["n"] is None
