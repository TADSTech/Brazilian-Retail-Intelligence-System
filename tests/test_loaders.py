from __future__ import annotations

import pandas as pd

from etl.config import TABLE_ORDER
from etl.loaders import Loader, records_for_json


class FakeLoader(Loader):
    def __init__(self, counts: dict[str, int] | None = None, full_reload: bool = False):
        self.calls: list[tuple[str, int]] = []
        self._counts = counts or {}
        self.full_reload = full_reload

    def row_count(self, table: str) -> int:
        return self._counts.get(table, -1)

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


def test_loader_skips_tables_already_loaded():
    loader = FakeLoader(counts={"orders": 10, "customers": 1})
    data = {
        "orders": pd.DataFrame({"x": range(10)}),
        "customers": pd.DataFrame({"x": [1, 2]}),
    }
    results = loader.load(data, tables=["orders", "customers"])
    assert [c[0] for c in loader.calls] == ["customers"]
    assert results["orders"] == 0
    assert results["customers"] == 2


def test_loader_upserts_partially_loaded_table():
    loader = FakeLoader(counts={"orders": 3})
    data = {"orders": pd.DataFrame({"x": range(10)})}
    results = loader.load(data, tables=["orders"])
    assert loader.calls == [("orders", 10)]
    assert results["orders"] == 10


def test_loader_full_reload_disables_skip():
    loader = FakeLoader(counts={"orders": 100}, full_reload=True)
    data = {"orders": pd.DataFrame({"x": range(10)})}
    results = loader.load(data, tables=["orders"])
    assert loader.calls == [("orders", 10)]
    assert results["orders"] == 10


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


def test_records_for_json_converts_timestamps_in_object_columns():
    # nat_to_none() casts datetime columns with NaT to object dtype holding
    # pd.Timestamp values — those must still serialize to ISO strings.
    df = pd.DataFrame(
        {
            "ts": pd.Series(
                [pd.Timestamp("2018-01-01T10:00:00"), None], dtype="object"
            ),
        }
    )
    records = records_for_json(df)
    assert records[0]["ts"] == "2018-01-01T10:00:00"
    assert records[1]["ts"] is None
