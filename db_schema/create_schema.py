"""Create the local PostgreSQL schema. Run: python -m db_schema.create_schema"""

from __future__ import annotations

import logging

from .models import Base, engine

logger = logging.getLogger(__name__)


def create_database_schema() -> None:
    """Create every table defined in db_schema.models."""
    Base.metadata.create_all(engine)
    logger.info("Database schema created.")


def check_schema_created() -> bool:
    """True if the customers table already exists."""
    from sqlalchemy import inspect

    return inspect(engine).has_table("customers")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    create_database_schema()
