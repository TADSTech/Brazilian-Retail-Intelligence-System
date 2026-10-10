from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from api.schemas import OrderGenRequest, OrderGenResponse
from ordergen.pipeline import generate_and_load

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])


def _run_order_gen_task(gen, count: int) -> None:
    try:
        results = generate_and_load(gen, count)
        logger.info("Generated and loaded orders: %s", results)
    except Exception:
        logger.exception("Order generation task failed")


@router.post("/generate", response_model=OrderGenResponse)
async def trigger_order_gen(
    request: OrderGenRequest, background_tasks: BackgroundTasks, req: Request
) -> OrderGenResponse:
    gen = getattr(req.app.state, "generator", None)
    if gen is None:
        raise HTTPException(
            status_code=503,
            detail="Order generator unavailable. Check SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY.",
        )
    background_tasks.add_task(_run_order_gen_task, gen, request.count)
    return OrderGenResponse(message=f"Order generation task for {request.count} orders started in background")
