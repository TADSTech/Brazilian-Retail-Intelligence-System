# Architecture

## Overview

BRIS loads the Olist retail dataset into PostgreSQL (Supabase in production), exposes a control API over the pipeline, and generates synthetic orders that respect the schema's foreign keys. Three deployable pieces: the ETL library, the FastAPI service, and the React dashboard.

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data | pandas, NumPy |
| API | FastAPI, Uvicorn, Pydantic v2 |
| ORM | SQLAlchemy 2.x |
| Warehouse | Supabase (PostgreSQL) via REST, or local Postgres |
| Synthetic data | Faker (pt_BR), Markov chain text model |
| Frontend | React 19, Vite, Tailwind 4, Supabase JS |
| Tests | pytest |

## Directory structure

```text
etl/
  config.py          # env settings, source file map, FK load order
  extract.py         # CSV read with encoding fallback
  pipeline.py        # extract → transform → load orchestration
  loaders.py         # Loader ABC, SupabaseLoader, PostgresLoader
  transform/         # one pure function per table + shared helpers
  __main__.py        # python -m etl
api/
  main.py            # app + lifespan (generator init)
  schemas.py         # request/response models
  routers/           # health, etl, orders
ordergen/
  generator.py       # trains on live tables, emits DataFrames
  markov.py          # review text model
  pipeline.py        # generate → transform → load
  main.py, backfill.py
db_schema/
  models.py          # ORM models (single source of table DDL)
  create_schema.py   # local DDL
  setup_constraints.py
  dbmanip.py         # per-table load helpers
tests/               # pure unit tests
```

## Key flows

### ETL run

1. `POST /etl/run` (or `python -m etl`) schedules a background task.
2. `etl.pipeline.extract_and_transform` reads the eight CSVs from `data/`.
3. Each frame passes through its transform (type casting, state mapping, timezone stripping, dedupe).
4. `get_loader()` picks `SupabaseLoader` or `PostgresLoader` from `ETL_BACKEND`.
5. `Loader.load` writes tables in FK order (`TABLE_ORDER`), batching upserts of 1000 rows.

### Synthetic order generation

1. `OrderGenerator.train()` pulls product IDs, seller IDs, and location samples from Supabase; prices from recent `order_items`; review text from the reviews CSV when present.
2. `generate_orders(n)` emits `customers → orders → order_items → payments → reviews` with consistent IDs and dates.
3. The production transformers clean the frames; the loader upserts them.

Failure to train disables `/orders/generate` (503) but leaves the API up.

### Dashboard

The dashboard queries Supabase directly with the publishable key and calls the API only for health/control. Vercel hosts it separately.

## Configuration

| File | Purpose |
|---|---|
| `.env` | Secrets and backend choice (gitignored) |
| `etl/config.py` | Reads env, defines `SOURCE_FILES` and `TABLE_ORDER` |
| `Dockerfile` | Python 3.12-slim image running uvicorn |
| `.github/workflows/scheduler.yml` | Hourly `POST /orders/generate` against deployment |

## Deployment

Backend: `./run_docker.sh` (builds the image, passes `--env-file .env`, exposes 8000).
Frontend: `dashboard/` deploys to Vercel (`dashboard/vercel.json`).
The GitHub Actions workflow needs a `BACKEND_URL` secret pointing at the deployed API.
