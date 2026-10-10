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
| Dashboard | `dashboard/` | React frontend (separate deploy) |
| Tests | `tests/` | Unit tests for transforms, extract, loader order, Markov |

## The data

The Olist dataset is a real Brazilian e-commerce marketplace covering 2016–2018. It ships as nine flat CSVs that model a complete order lifecycle — who bought, what they bought, how they paid, what they thought, and where it shipped from and to:

| CSV | Rows | What it holds |
|---|---|---|
| `olist_orders_dataset.csv` | 99,441 | One row per order: status, purchase/approval/delivery timestamps, estimated delivery |
| `olist_order_items_dataset.csv` | 112,650 | Line items: product, seller, price, freight |
| `olist_order_payments_dataset.csv` | 103,886 | Payment type (credit/boleto/voucher), instalments, value |
| `olist_order_reviews_dataset.csv` | 99,224 | 1–5 star score + free-text comment (Portuguese) |
| `olist_products_dataset.csv` | 32,951 | Category (PT), dimensions, weight, photo count |
| `olist_sellers_dataset.csv` | 3,095 | Seller location (zip, city, state) |
| `olist_customers_dataset.csv` | 99,441 | Customer location + `customer_unique_id` for repeat-buyer analysis |
| `olist_geolocation_dataset.csv` | 1,000,163 | Zip-code-prefix → lat/lng lookup (deduplicated on load) |
| `product_category_name_translation.csv` | 71 | PT → EN category labels |

After transforms the platform lands at **1,287,963 rows across 8 tables** — geolocation is deduplicated from ~1M to 738,332 rows (one deterministic id per unique row), and order reviews keep all score-only entries (98,167 after soft-deduping). The dataset is not committed to git — download the zip from the [GitHub release](../../releases) and extract into `data/`.

## How the ETL works

The pipeline is one package, `etl/`, run as `python -m etl`. Three stages:

**Extract** (`etl/extract.py`) — reads each CSV from `data/` into a pandas DataFrame. Missing files fail loudly; there is no silent skip.

**Transform** (`etl/transform/`) — one module per table, each a pure function `DataFrame → DataFrame` with no I/O and no side effects. That makes every rule unit-testable in isolation. Shared logic lives in `etl/transform/common.py`:

- State initials (`SP`, `RJ`, …) mapped to full UTF-8 names via a single source-of-truth dict
- Timezone-naive timestamps (Olist mixes naive and aware datetimes; all are stripped to naive UTC)
- Row dedupe and a light `dropna` threshold (`finalize()`)
- PT → EN product category names joined from the translation CSV (non-fatal if the file is absent)
- `geolocation` deduplicated on zip-code prefix, keeping one lat/lng per prefix

**Load** (`etl/loaders.py`) — a small `Loader` ABC with two backends selected by `ETL_BACKEND`:

- `SupabaseLoader` — converts each DataFrame to JSON-safe records (datetimes → ISO 8601, NaN/NaT → `null`), then batch-upserts through the Supabase REST client with `return=minimal` (no echoed rows), retries on transient failures, and concurrent batch requests. Defaults: 5,000 rows/request (`ETL_BATCH_SIZE`) across 2 workers (`ETL_LOAD_WORKERS`), 120 s read timeout. This is the production/Docker path; it needs only `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`.
- `PostgresLoader` — bulk insert via SQLAlchemy against `DATABASE_URL`. With `--full-reload` it truncates children before parents to respect FKs. This is the local-dev path.

Both honour the same FK-safe table order declared once in `etl/config.py::TABLE_ORDER`:

```text
geolocation → customers → sellers → products → orders → order_items → order_payments → order_reviews
```

Loads are **idempotent** and **incremental**: before writing a table the loader counts the target rows and skips the table when it is already fully loaded (`--full-reload` forces a rewrite). The Supabase path upserts on primary keys, so even partial re-runs never duplicate rows. Re-running a finished pipeline takes seconds, not hours.

Run a full load or a subset:

```bash
python -m etl                          # everything; already-loaded tables are skipped
python -m etl --tables orders order_items
python -m etl --full-reload            # force rewrite (postgres: truncate + reload)
```

## The API

FastAPI app in `api/`, three endpoints:

| Method | Path | Body | Notes |
|---|---|---|---|
| GET | `/health` | — | `{status, generator_ready}` |
| POST | `/etl/run` | `{full_reload?, tables?}` | Runs the pipeline in a background task |
| POST | `/orders/generate` | `{count}` | 503 if the generator failed to train |

Interactive docs at `/docs`. The ETL trigger runs in-process as a FastAPI `BackgroundTasks` job — no external queue — which keeps the deploy story simple (single container via `run_docker.sh`).

## Synthetic order generator

`ordergen/` produces referentially-consistent fake orders so the dashboard has live data between real ETL runs:

1. **Train on real distributions** — product/seller/location IDs and payment patterns are sampled from the live Supabase tables, so every synthetic order resolves against real foreign keys.
2. **Markov review text** (`ordergen/markov.py`) — a simple order-N word model trained on the Portuguese review comments, generating plausible-sounding review bodies.
3. **Write-through the same loader** — synthetic rows land via the same `SupabaseLoader` upsert path as the real pipeline.

```bash
python -m ordergen.main --count 100
python -m ordergen.backfill --count 5000
```

## Frontend (`dashboard/`)

A separate React + Vite + TypeScript app. It authenticates against Supabase with the **anon key** (read-only, RLS-safe) and hits the API only for control actions (trigger ETL, generate orders).

**Stack:** React 19, Vite 7, TypeScript 5.9, Tailwind CSS 4, shadcn/ui primitives, Recharts + Plotly for charts, React Router 7.

**Routes:**

| Path | Page | What it does |
|---|---|---|
| `/` | `Home.tsx` | Marketing/landing page with architecture overview and quick-start |
| `/signin` | `SignIn.tsx` | Supabase email/password sign-in |
| `/dashboard` | `Dashboard.tsx` | Auth-gated app shell with sidebar tabs |

**Dashboard tabs** (`components/dashboard/tabs/`):

- **Overview** — KPI cards (total revenue, orders, customers, avg ticket), revenue-over-time chart, order-status breakdown, category performance, customer map (Plotly Brazil geo)
- **Analytics** — payment insights, instalment distribution, review-score histogram
- **Customers** — repeat-buyer rate, state-level heat, top customer states
- **Products** — top categories by revenue and volume, freight vs price scatter
- **Settings** — ETL trigger, order-generator trigger, pipeline status

**Data access** (`hooks/use-dashboard-data.ts`) — one hook fetches all dashboard aggregates via the Supabase JS client with batched pagination (`fetchInBatches`), so the page works on the anon key alone without a Postgres connection string. Loading states use skeleton components; errors surface with a retry action.

The dashboard has its own `.env` (Vite only reads `dashboard/.env` — see `dashboard/.env.example`):

```bash
VITE_SUPABASE_URL=https://<ref>.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_...
```

Run it:

```bash
cd dashboard
npm install
npm run dev        # → http://localhost:5173
```

## Quick start

### 1. Environment

```bash
cp .env.example .env
# fill in SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (or DATABASE_URL for local Postgres)

cp dashboard/.env.example dashboard/.env
# fill in VITE_SUPABASE_URL + VITE_SUPABASE_ANON_KEY (the dashboard reads its own .env)
```

`.env` is gitignored. Never commit it. Service-role keys bypass row-level security; treat them like passwords.

### 2. Dataset

Download `brazilian-ecommerce.zip` from the [GitHub release](../../releases) and extract it into `data/` (the folder ships with the repo; the zip contains the CSVs at its root, not a `data/` folder):

```bash
unzip brazilian-ecommerce.zip -d data/        # macOS/Linux
# PowerShell: Expand-Archive brazilian-ecommerce.zip -DestinationPath data
```

The CSVs are gitignored. Expect 9 files in `data/` — see [`data/README.md`](data/README.md) or [dataset setup](docs/dataset_setup.md) for the exact list (or the Kaggle alternative).

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

## Supabase without a DB password

The service key can load data but cannot create tables. To set up a fresh Supabase project once, without the database password:

1. Create a personal access token: Dashboard → **Account settings → Access Tokens → New token**
2. Add it to `.env` (see `.env.example`): `SUPABASE_ACCESS_TOKEN=sbp_...`
3. Run the one-time setup:

```bash
python -m db_schema.create_supabase_schema
```

4. Revoke the token in the dashboard — it is only needed for that one call.

This runs [`db_schema/supabase_schema.sql`](db_schema/supabase_schema.sql) (idempotent: tables, FKs, indexes, grants) via the Management API. Alternatively paste the same file into the SQL Editor (token-free). After that, `python -m etl` works with the service key alone — `DATABASE_URL` is not consulted when `ETL_BACKEND=supabase`.

## Analytical SQL (`sql/`)

Ready-made queries the dashboard and docs draw on:

| File | Answers |
|---|---|
| `executive_overview.sql` | Headline KPIs across the whole dataset |
| `revenue_over_time.sql` | Monthly revenue and order volume trend |
| `sales_revenue.sql` | Revenue split by product category |
| `product_performance.sql` | Best and worst products by freight-adjusted revenue |
| `customer_behavior.sql` | Repeat purchase rate, basket size distribution |
| `customer_satisfaction.sql` | Review score distribution and correlates |
| `logistics_efficiency.sql` | Delivery time vs estimate, late-delivery rate by state |
| `payment_insights.sql` | Payment type mix, instalment behaviour |

## Design notes

- **One ETL package.** Load target is configuration (`ETL_BACKEND`), not a fork of the codebase.
- **FK-safe load order** is declared once (`etl/config.py::TABLE_ORDER`): geolocation → customers → sellers → products → orders → order_items → order_payments → order_reviews.
- **Transforms are pure.** Each takes a DataFrame and returns a cleaned DataFrame. Shared rules (state mapping, timezone stripping, dedupe) live in `etl/transform/common.py`.
- **Idempotent loads.** The Supabase path upserts on primary keys, so re-runs do not duplicate rows.
- **Generator stays referentially consistent.** Synthetic orders sample product, seller, and location IDs from the database so foreign keys resolve.
- **Dashboard uses the anon key.** Read-only access through PostgREST; the service-role key never reaches the browser.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API reference](docs/API_ENDPOINTS.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [ETL setup](docs/etl_setup.md)
- [Dataset setup](docs/dataset_setup.md)

## Author

**TADSTech** — full-stack data engineering.
