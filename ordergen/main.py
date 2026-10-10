"""CLI: generate synthetic orders and upsert them.

    python -m ordergen.main --count 100
"""

from __future__ import annotations

import argparse
import logging
import sys

from etl.logging_config import configure_logging

from .pipeline import build_generator, generate_and_load

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = argparse.ArgumentParser(prog="ordergen", description="Generate synthetic orders.")
    parser.add_argument("--count", type=int, default=10, help="Number of orders to generate.")
    parser.add_argument("--data-dir", default=None, help="Optional CSV dir for Markov training.")
    args = parser.parse_args(argv)

    try:
        gen = build_generator(args.data_dir)
        results = generate_and_load(gen, args.count)
        logger.info("Loaded synthetic orders: %s", results)
    except Exception:
        logger.exception("Order generation failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
