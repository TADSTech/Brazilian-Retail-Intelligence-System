# ETL Setup

Single pipeline in `etl/`. The load backend is a configuration choice, not a fork of the code.

## Pipeline stages

1. **Extract** (`etl/extract.py`) — reads CSVs with an encoding fallback chain (`utf-8`, `latin1`, `cp1252`, `iso-8859-1`).
2. **Transform** (`etl/transform/`) — one pure module per table: type casting, Brazilian state mapping, timezone removal, dedupe.
3. **Load** (`etl/loaders.py`) — `SupabaseLoader` (batched REST upsert, 1000 rows per call) or `PostgresLoader` (SQLAlchemy bulk insert, optional truncate).

## Backends

Set `ETL_BACKEND` in `.env`:

- `supabase` (default) — needs `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
- `postgres` — needs `DATABASE_URL`

## Commands

```bash
python -m etl                          # all eight tables
python -m etl --tables orders order_items
python -m etl --full-reload            # postgres only: truncate first
python -m etl --data-dir /path/to/csvs # override DATA_DIR
```

Via API:

```bash
curl -X POST http://localhost:8000/etl/run \
  -H "Content-Type: application/json" \
  -d '{"full_reload": false, "tables": ["orders"]}'
```

## Source files

Expected in `data/` (or `DATA_DIR`):

```text
olist_customers_dataset.csv          geolocation_zip_code_prefix...
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv   # optional, enables English categories
```

Get them from the [GitHub release](../../releases) or Kaggle.

## Failure modes

| Symptom | Fix |
|---|---|
| `Data directory not found` | Extract CSVs into `data/` or set `DATA_DIR` |
| `SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set` | Fill in `.env` |
| `Schema missing` (postgres) | `python -m db_schema.create_schema` |
| Duplicate rows after re-run | Should not happen: Supabase path upserts on PK. Check for PK mismatches in transforms. |
