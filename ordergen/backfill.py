"""CLI: backfill synthetic historical orders (fills the gap after the Olist window).

    python -m ordergen.backfill --count 5000
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime

from etl.logging_config import configure_logging

from .pipeline import build_generator, generate_and_load

logger = logging.getLogger(__name__)

# Olist dataset ends around 2018-10-18.
BACKFILL_START = datetime(2018, 10, 18)


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = argparse.ArgumentParser(prog="ordergen.backfill", description="Backfill synthetic history.")
    parser.add_argument("--count", type=int, default=5000, help="Total orders to generate.")
    parser.add_argument("--data-dir", default=None, help="Optional CSV dir for Markov training.")
    args = parser.parse_args(argv)

    end_date = datetime.now()
    batch_size = 1000
    generated = 0
    try:
        gen = build_generator(args.data_dir)
        while generated < args.count:
            current = min(batch_size, args.count - generated)
            logger.info("Backfill batch %d/%d", generated + current, args.count)
            generate_and_load(gen, current, start_date=BACKFILL_START, end_date=end_date)
            generated += current
        logger.info("Backfill complete: %d orders", generated)
    except Exception:
        logger.exception("Backfill failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
