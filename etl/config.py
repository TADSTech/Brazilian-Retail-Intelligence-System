"""Environment-driven configuration for the ETL package."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Canonical CSV names shipped with the Olist dataset.
SOURCE_FILES: dict[str, str] = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}

# Load order respects foreign keys: parents before children.
TABLE_ORDER: tuple[str, ...] = (
    "geolocation",
    "customers",
    "sellers",
    "products",
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
)

CATEGORY_TRANSLATION_FILE = "product_category_name_translation.csv"


@dataclass(frozen=True)
class Settings:
    backend: str = field(default_factory=lambda: os.getenv("ETL_BACKEND", "supabase").lower())
    supabase_url: str | None = field(default_factory=lambda: os.getenv("SUPABASE_URL"))
    supabase_service_role_key: str | None = field(
        default_factory=lambda: os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPERKEY")
    )
    database_url: str | None = field(default_factory=lambda: os.getenv("DATABASE_URL"))
    data_dir: Path = field(default_factory=lambda: Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data")))
    batch_size: int = field(default_factory=lambda: int(os.getenv("ETL_BATCH_SIZE", "5000")))
    load_workers: int = field(default_factory=lambda: int(os.getenv("ETL_LOAD_WORKERS", "2")))

    def require_supabase(self) -> tuple[str, str]:
        if not self.supabase_url or not self.supabase_service_role_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set for the supabase backend."
            )
        return self.supabase_url, self.supabase_service_role_key

    def require_postgres(self) -> str:
        if not self.database_url:
            raise ValueError("DATABASE_URL must be set for the postgres backend.")
        return self.database_url


settings = Settings()
