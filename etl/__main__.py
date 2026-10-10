"""CLI entry point: python -m etl"""

from __future__ import annotations

import argparse
import logging
import sys

from .config import TABLE_ORDER
from .logging_config import configure_logging
from .pipeline import run


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = argparse.ArgumentParser(prog="etl", description="Run the Olist retail ETL pipeline.")
    parser.add_argument("--data-dir", default=None, help="Directory containing the Olist CSVs.")
    parser.add_argument("--full-reload", action="store_true", help="Truncate target tables first (postgres backend).")
    parser.add_argument(
        "--tables",
        nargs="+",
        choices=TABLE_ORDER,
        metavar="TABLE",
        help=f"Load only these tables (any of {', '.join(TABLE_ORDER)}).",
    )
    args = parser.parse_args(argv)

    try:
        run(data_dir=args.data_dir, tables=args.tables, full_reload=args.full_reload)
    except Exception:
        logging.getLogger(__name__).exception("ETL failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
