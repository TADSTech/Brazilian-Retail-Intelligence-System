"""Extract -> transform orchestration shared by the CLI and the API."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from .config import SOURCE_FILES, settings
from .extract import extract_csv
from .loaders import Loader, get_loader
from .transform import TRANSFORMS

logger = logging.getLogger(__name__)


def extract_and_transform(data_dir: str | Path | None = None) -> dict[str, pd.DataFrame]:
    """Read every source CSV, run its transform, return {table: DataFrame}."""
    data_dir = Path(data_dir or settings.data_dir)
    if not data_dir.is_dir():
        raise FileNotFoundError(
            f"Data directory not found: {data_dir}. "
            "Download the Olist CSVs from the GitHub release and extract them there."
        )

    transformed: dict[str, pd.DataFrame] = {}
    for table, filename in SOURCE_FILES.items():
        path = data_dir / filename
        logger.info("Extracting %s", path.name)
        raw = extract_csv(path)
        if table == "products":
            transformed[table] = TRANSFORMS[table](raw, data_dir=str(data_dir))
        else:
            transformed[table] = TRANSFORMS[table](raw)
        logger.info("Transformed %s: %d rows", table, len(transformed[table]))
    return transformed


def run(
    data_dir: str | Path | None = None,
    tables: list[str] | None = None,
    full_reload: bool = False,
    loader: Loader | None = None,
) -> dict[str, int]:
    """Run the full pipeline and return per-table row counts."""
    logger.info("ETL start (backend=%s, full_reload=%s, tables=%s)", settings.backend, full_reload, tables)
    transformed = extract_and_transform(data_dir)
    active = loader or get_loader(full_reload=full_reload)
    results = active.load(transformed, tables=tables)
    logger.info("ETL done: %s", results)
    return results
