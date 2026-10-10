"""CSV extraction with encoding fallbacks."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

ENCODINGS = ("utf-8", "latin1", "cp1252", "iso-8859-1")


def extract_csv(path: str | Path) -> pd.DataFrame:
    """Read a CSV file, trying several encodings until one decodes cleanly."""
    path = Path(path)
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Only CSV files are supported, got: {path.suffix or path.name}")
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    last_error: Exception | None = None
    for encoding in ENCODINGS:
        try:
            df = pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue

        if df.empty:
            logger.warning("%s is empty", path.name)
        elif df.shape[1] == 0:
            logger.warning("%s has no columns", path.name)
        return df

    raise UnicodeError(f"Could not decode {path} with encodings {ENCODINGS}: {last_error}")
