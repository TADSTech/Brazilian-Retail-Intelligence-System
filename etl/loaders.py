"""Load strategies selected by ETL_BACKEND.

supabase: batched upsert over the REST API (production / Docker path).
postgres: bulk insert via SQLAlchemy against DATABASE_URL (local path).
"""

from __future__ import annotations

import logging
import time
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
            elif isinstance(value, pd.Timestamp):
                # Object-dtype columns (e.g. after nat_to_none) hold Timestamps,
                # not datetime64 — convert those too.
                row[key] = value.isoformat()
            elif not isinstance(value, (str, int, float, bool)) and pd.isna(value):
                row[key] = None
    return records


class Loader(ABC):
    """Minimal loader contract: upsert one table, honour FK order."""

    #: When True, tables whose target row count already matches the source are skipped.
    #: full_reload disables the skip (postgres truncates; supabase force re-upserts).
    full_reload: bool = False

    @abstractmethod
    def upsert(self, table: str, df: pd.DataFrame) -> int:
        """Write rows for `table`. Returns rows written."""

    def row_count(self, table: str) -> int:
        """Rows currently in the target table; -1 when unknown (never skips)."""
        return -1

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
            existing = self.row_count(table) if not self.full_reload else -1
            if existing >= len(df):
                logger.info(
                    "Skipping %s (already loaded: %d rows in target, %d in source)",
                    table,
                    existing,
                    len(df),
                )
                results[table] = 0
                continue
            results[table] = self.upsert(table, df)
        return results


class SupabaseLoader(Loader):
    """Batched upsert through the Supabase REST client.

    Speed levers (env): ``ETL_BATCH_SIZE`` rows per request (default 5000) and
    ``ETL_LOAD_WORKERS`` concurrent batch requests (default 2). Batches are
    independent PK upserts, so concurrency is safe; failed batches retry up to
    four times with backoff (upserts are idempotent).
    """

    RETRY_ATTEMPTS = 4

    def __init__(
        self,
        batch_size: int | None = None,
        workers: int | None = None,
        full_reload: bool = False,
    ):
        import httpx
        from supabase import create_client

        url, key = settings.require_supabase()
        self.client = create_client(url, key)
        self.batch_size = batch_size or settings.batch_size
        self.workers = workers or settings.load_workers
        self.full_reload = full_reload
        # Large tables (geolocation ~740k rows) exceed the default 5s read timeout.
        self.client.postgrest.session.timeout = httpx.Timeout(120.0, connect=10.0)

    def row_count(self, table: str) -> int:
        res = self.client.table(table).select("*", count="exact", head=True).execute()
        return res.count or 0

    def _write_batch(self, table: str, batch: list[dict]) -> None:
        for attempt in range(1, self.RETRY_ATTEMPTS + 1):
            try:
                # returning=minimal skips the echoed RETURNING payload.
                self.client.table(table).upsert(batch, returning="minimal").execute()
                return
            except Exception:
                if attempt == self.RETRY_ATTEMPTS:
                    raise
                logger.warning(
                    "%s batch failed (attempt %d/%d), backing off",
                    table,
                    attempt,
                    self.RETRY_ATTEMPTS,
                )
                time.sleep(2 ** (attempt - 1))

    def upsert(self, table: str, df: pd.DataFrame) -> int:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        records = records_for_json(df)
        total = len(records)
        batches = [records[i : i + self.batch_size] for i in range(0, total, self.batch_size)]
        workers = max(1, min(self.workers, len(batches)))
        logger.info(
            "Upserting %d rows into %s in %d batches (%d workers)",
            total,
            table,
            len(batches),
            workers,
        )
        done = 0
        if workers == 1:
            for batch in batches:
                self._write_batch(table, batch)
                done += 1
                if done % 20 == 0 or done == len(batches):
                    logger.info("  %s: %d/%d batches", table, done, len(batches))
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(self._write_batch, table, batch) for batch in batches]
                for future in as_completed(futures):
                    future.result()  # re-raise the first failure
                    done += 1
                    if done % 20 == 0 or done == len(batches):
                        logger.info("  %s: %d/%d batches", table, done, len(batches))
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
