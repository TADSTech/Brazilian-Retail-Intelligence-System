"""ETL pipeline for the Brazilian E-Commerce public dataset.

Public entry points:
    python -m etl                # full load (extract -> transform -> load)
    python -m etl --incremental  # upsert only
    python -m etl --tables orders order_items
"""
