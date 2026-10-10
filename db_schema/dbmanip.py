"""Bulk-load helpers for the local PostgreSQL schema.

Prefer `etl.loaders.PostgresLoader` for new code; these functions remain
for scripts that need per-table control.
"""

from __future__ import annotations

import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from .create_schema import check_schema_created
from .models import MODELS, engine

logger = logging.getLogger(__name__)
Session = sessionmaker(bind=engine)


def load_table(table: str, df: pd.DataFrame, full_reload: bool = False) -> int:
    """Insert one table's rows. Optionally truncate first (parent tables only)."""
    if not check_schema_created():
        raise RuntimeError("Schema missing. Run `python -m db_schema.create_schema` first.")
    if table not in MODELS:
        raise KeyError(f"Unknown table {table!r}. Known: {sorted(MODELS)}")

    session = Session()
    try:
        if full_reload:
            session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
        records = df.to_dict("records")
        session.bulk_insert_mappings(MODELS[table], records)
        session.commit()
        logger.info("Loaded %d rows into %s", len(records), table)
        return len(records)
    except Exception:
        session.rollback()
        logger.exception("Failed loading %s", table)
        raise
    finally:
        session.close()


def load_customers(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("customers", df, full_reload)


def load_geolocation(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("geolocation", df, full_reload)


def load_orders(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("orders", df, full_reload)


def load_order_items(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("order_items", df, full_reload)


def load_order_payments(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("order_payments", df, full_reload)


def load_order_reviews(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("order_reviews", df, full_reload)


def load_products(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("products", df, full_reload)


def load_sellers(df: pd.DataFrame, full_reload: bool = False) -> int:
    return load_table("sellers", df, full_reload)
