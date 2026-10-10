"""Brazilian Retail Intelligence API.

Run locally:  uvicorn api.main:app --reload
Run in Docker: container CMD starts uvicorn on :8000.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import etl, health, orders
from etl.logging_config import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    app.state.generator = None
    app.state.generator_ready = False
    try:
        from ordergen.generator import OrderGenerator

        gen = OrderGenerator()
        gen.train()
        app.state.generator = gen
        app.state.generator_ready = True
        logger.info("Order generator ready")
    except Exception:
        # API stays up; /orders/generate returns 503 until credentials are fixed.
        logger.exception("Order generator failed to initialize; /orders/generate disabled")
    yield


app = FastAPI(
    title="Brazilian Retail Intelligence API",
    description="ETL control plane and synthetic order generation for the Olist retail dataset.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(etl.router)
app.include_router(orders.router)
