# API Endpoints

Base URL: `http://localhost:8000` (Docker) or wherever the backend deploys.
Interactive documentation: `/docs` (Swagger UI) and `/redoc`.
Authentication: none. Put a reverse proxy or API key in front before exposing this publicly.

## `GET /health`

Liveness probe plus generator state.

**Response 200**
```json
{ "status": "healthy", "generator_ready": true }
```

`generator_ready` is `false` when the order generator failed to train at startup (usually bad or missing Supabase credentials).

## `POST /etl/run`

Runs the full ETL pipeline in a background task. The request returns immediately.

**Body**
```json
{
  "full_reload": false,
  "tables": ["orders", "order_items"]
}
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `full_reload` | bool | `false` | Truncates target tables first. Postgres backend only. |
| `tables` | array or null | `null` (all eight) | Any of `geolocation`, `customers`, `sellers`, `products`, `orders`, `order_items`, `order_payments`, `order_reviews`. |

**Response 200**
```json
{ "message": "ETL task started in background", "detail": null }
```

**Errors**
- `422` — validation (unknown table name, wrong types)

Task outcome lands in the service logs, not the response body.

## `POST /orders/generate`

Generates synthetic orders and upserts them.

**Body**
```json
{ "count": 10 }
```

| Field | Type | Default | Constraints |
|---|---|---|---|
| `count` | int | `10` | 1 ≤ count ≤ 10000 |

**Response 200**
```json
{ "message": "Order generation task for 10 orders started in background" }
```

**Errors**
- `503` — generator not ready (credentials or training failure)
- `422` — validation

## Error format

FastAPI defaults: `{ "detail": "<message>" }` with the appropriate status code.
