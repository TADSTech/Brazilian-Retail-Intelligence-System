from __future__ import annotations

import pandas as pd
import pytest

from etl.extract import extract_csv


def test_extract_csv_reads_utf8(tmp_path):
    path = tmp_path / "sample.csv"
    path.write_text("a,b\n1,2\n", encoding="utf-8")
    df = extract_csv(path)
    assert list(df.columns) == ["a", "b"]
    assert len(df) == 1


def test_extract_csv_rejects_non_csv(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="CSV"):
        extract_csv(path)


def test_extract_csv_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_csv(tmp_path / "nope.csv")


def test_extract_csv_latin1_fallback(tmp_path):
    path = tmp_path / "latin.csv"
    path.write_bytes("city\nSão Paulo\n".encode("latin1"))
    df = extract_csv(path)
    assert df.iloc[0, 0] == "São Paulo"
