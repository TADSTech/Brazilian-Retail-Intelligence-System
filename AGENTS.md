# AGENTS.md

Guidance for AI agents and new contributors working in this repository.

## What this repo is

A retail data platform built on the public Olist Brazilian e-commerce dataset:

- `etl/` — extract, transform, load pipeline (single package, two load backends)
- `api/` — FastAPI control plane (trigger ETL, generate synthetic orders)
- `ordergen/` — synthetic order generator trained on live table distributions
- `db_schema/` — SQLAlchemy models, local schema tooling, constraint setup
- `dashboard/` — React frontend (separate deploy; do not restyle without asking)
- `sql/` — analytical queries used by the dashboard/docs
- `tests/` — pytest suite for pure transforms, extract, loaders, Markov model

## Commands

```bash
# Install
pip install -r requirements-dev.txt

# Tests (run these before claiming a change works)
python -m pytest tests -q

# ETL CLI (needs data/ CSVs + credentials)
python -m etl --help
python -m etl                       # full load
python -m etl --tables orders order_items

# Synthetic orders
python -m ordergen.main --count 100
python -m ordergen.backfill --count 5000

# API
uvicorn api.main:app --reload

# Local Postgres schema
python -m db_schema.create_schema
python -m db_schema.setup_constraints

# Docker
./run_docker.sh
```

## Layout rules

- One ETL package: `etl/`. Do not create `etl_local/`, `etl_prod/`, or per-environment copies.
- Load backend is chosen by `ETL_BACKEND` (`supabase` | `postgres`) in `etl/config.py`.
- Transform functions stay pure: DataFrame in, DataFrame out. Shared helpers live in `etl/transform/common.py`.
- Table load order is FK-safe and defined once in `etl/config.py::TABLE_ORDER`.
- Logging uses the stdlib `logging` module. Never reintroduce print-based log helpers.
- Secrets come from environment variables only. Never hardcode URLs, passwords, or keys. `.env` is gitignored; `.env.example` documents the variable names.

## Environment variables

| Variable | Used by |
|---|---|
| `ETL_BACKEND` | loader selection (`supabase` default) |
| `SUPABASE_URL` | Supabase loader + order generator |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase loader (`SUPERKEY` accepted as legacy alias) |
| `DATABASE_URL` | postgres loader + db_schema tooling |
| `DATA_DIR` | optional override for the `data/` CSV directory |
| `ETL_BATCH_SIZE` | Supabase upsert batch size (default 5000) |
| `ETL_LOAD_WORKERS` | concurrent batch requests during Supabase load (default 2) |

## Conventions

- Python 3.10+, type hints on public functions, `from __future__ import annotations`.
- FastAPI: routers under `api/routers/`, Pydantic models in `api/schemas.py`, lifespan in `api/main.py`.
- Tests: pure unit tests only (no live DB, no network). Put them in `tests/`.
- The dashboard is TypeScript/React. Backend changes must not require dashboard edits unless the API contract changes.
- Docs live in `docs/` as Markdown. PDFs are optional exports, not the source of truth.

## Before you finish a change

1. `python -m pytest tests -q` passes.
2. `python -c "from api.main import app"` succeeds with dummy Supabase env vars set.
3. No new secrets, no `.env` commits, no duplicate packages.
4. Grep for stale names (`etl_prod`, `etl_local`, `SUPERKEY` in docs) if you touched structure.
