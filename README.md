# Brazilian Retail Intelligence System (BRIS)

Data platform on the public [Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): an ETL pipeline, a FastAPI control plane, a synthetic order generator, and a React dashboard.

The backend is the product here. The dashboard reads the same Supabase tables the pipeline writes.

## Architecture

```text
data/*.csv ──► etl (extract → transform) ──► loaders ──► Supabase / local Postgres
                                                      ▲
FastAPI ──► POST /etl/run ────────────────────────────┤
         ──► POST /orders/generate ──► ordergen ──────┘
dashboard ──► Supabase (read) + API (control)
```

| Component | Path | Role |
|---|---|---|
| ETL | `etl/` | CSV extract, pure transforms, FK-ordered load |
| Loaders | `etl/loaders.py` | `SupabaseLoader` (batched REST upsert) and `PostgresLoader` (SQLAlchemy bulk insert) |
| API | `api/` | FastAPI: health, ETL trigger, synthetic order trigger |
| OrderGen | `ordergen/` | Samples real products/sellers/locations; Markov review text |
| Schema | `db_schema/` | SQLAlchemy models, local DDL, FKs/indexes, migration helpers |
| SQL | `sql/` | Analytical queries (revenue, logistics, satisfaction) |
| Tests | `tests/` | Unit tests for transforms, extract, loader order, Markov |

## Quick start

### 1. Environment

```bash
cp .env.example .env
# fill in SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (or DATABASE_URL for local Postgres)
```

`.env` is gitignored. Never commit it. Service-role keys bypass row-level security; treat them like passwords.

### 2. Dataset

Download the Olist CSVs from the [GitHub release](../../releases) and extract them into `data/`.

### 3. Backend

```bash
pip install -r requirements.txt

# Full pipeline
python -m etl

# Subset of tables
python -m etl --tables orders order_items

# Synthetic orders
python -m ordergen.main --count 100

# API
uvicorn api.main:app --reload
# → http://localhost:8000/docs
```

### 4. Docker

```bash
./run_docker.sh
curl http://localhost:8000/health
curl -X POST http://localhost:8000/orders/generate \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

### 5. Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q
```

## Local Postgres path

Set `ETL_BACKEND=postgres` and `DATABASE_URL`, then:

```bash
python -m db_schema.create_schema
python -m db_schema.setup_constraints
python -m etl --full-reload
```

## API

| Method | Path | Body | Notes |
|---|---|---|---|
| GET | `/health` | — | `{status, generator_ready}` |
| POST | `/etl/run` | `{full_reload?, tables?}` | Runs the pipeline in a background task |
| POST | `/orders/generate` | `{count}` | 503 if the generator failed to train |

Interactive docs at `/docs`.

## Design notes

- **One ETL package.** Load target is configuration (`ETL_BACKEND`), not a fork of the codebase.
- **FK-safe load order** is declared once (`etl/config.py::TABLE_ORDER`): geolocation → customers → sellers → products → orders → order_items → order_payments → order_reviews.
- **Transforms are pure.** Each takes a DataFrame and returns a cleaned DataFrame. Shared rules (state mapping, timezone stripping, dedupe) live in `etl/transform/common.py`.
- **Idempotent loads.** The Supabase path upserts on primary keys, so re-runs do not duplicate rows.
- **Generator stays referentially consistent.** Synthetic orders sample product, seller, and location IDs from the database so foreign keys resolve.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API reference](docs/API_ENDPOINTS.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [ETL setup](docs/etl_setup.md)
- [Dataset setup](docs/dataset_setup.md)

## Author

**TADSTech** — full-stack data engineering.
