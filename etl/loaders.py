"""Load strategies selected by ETL_BACKEND.

supabase: batched upsert over the REST API (production / Docker path).
postgres: bulk insert via SQLAlchemy against DATABASE_URL (local path).
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import pandas as pd

from .config import TABLE_ORDER, settings

logger = logging.getLogger(__name__)


def records_for_json(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame into JSON-safe records (datetimes -> ISO, NaN/NaT -> None)."""
    clean = df.copy()
    for col in clean.columns:
        if pd.api.types.is_datetime64_any_dtype(clean[col]):
            clean[col] = clean[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    records = clean.to_dict("records")
    for row in records:
        for key, value in row.items():
            if value is None or (isinstance(value, float) and pd.isna(value)) or value is pd.NaT:
                row[key] = None
            elif not isinstance(value, (str, int, float, bool)) and pd.isna(value):
                row[key] = None
    return records


class Loader(ABC):
    """Minimal loader contract: upsert one table, honour FK order."""

    @abstractmethod
    def upsert(self, table: str, df: pd.DataFrame) -> int:
        """Write rows for `table`. Returns rows written."""

    def load(
        self,
        transformed: dict[str, pd.DataFrame],
        tables: list[str] | None = None,
    ) -> dict[str, int]:
        """Load tables in FK-safe order. `tables` filters which keys to load."""
        selected = [t for t in TABLE_ORDER if tables is None or t in tables]
        results: dict[str, int] = {}
        for table in selected:
            df = transformed.get(table)
            if df is None or df.empty:
                logger.info("Skipping %s (no rows)", table)
                continue
            results[table] = self.upsert(table, df)
        return results


class SupabaseLoader(Loader):
    """Batched upsert through the Supabase REST client."""

    def __init__(self, batch_size: int | None = None):
        from supabase import create_client

        url, key = settings.require_supabase()
        self.client = create_client(url, key)
        self.batch_size = batch_size or settings.batch_size

    def upsert(self, table: str, df: pd.DataFrame) -> int:
        records = records_for_json(df)
        total = len(records)
        logger.info("Upserting %d rows into %s", total, table)
        for start in range(0, total, self.batch_size):
            batch = records[start : start + self.batch_size]
            self.client.table(table).upsert(batch).execute()
        return total


class PostgresLoader(Loader):
    """Bulk insert via SQLAlchemy. Truncates children first when full_reload=True."""

    def __init__(self, full_reload: bool = False):
        from sqlalchemy import text
        from sqlalchemy.orm import sessionmaker

        from db_schema.models import MODELS, engine

        self._text = text
        self.session_factory = sessionmaker(bind=engine)
        self.models = MODELS
        self.full_reload = full_reload

    def upsert(self, table: str, df: pd.DataFrame) -> int:
        model = self.models[table]
        records = df.to_dict("records")
        session = self.session_factory()
        try:
            if self.full_reload:
                session.execute(
                    self._text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
                )
            session.bulk_insert_mappings(model, records)
            session.commit()
            logger.info("Loaded %d rows into %s", len(records), table)
            return len(records)
        except Exception:
            session.rollback()
            logger.exception("Failed loading %s", table)
            raise
        finally:
            session.close()


def get_loader(full_reload: bool = False) -> Loader:
    backend = settings.backend
    if backend == "supabase":
        return SupabaseLoader()
    if backend == "postgres":
        return PostgresLoader(full_reload=full_reload)
    raise ValueError(f"Unknown ETL_BACKEND {backend!r}; expected 'supabase' or 'postgres'")
