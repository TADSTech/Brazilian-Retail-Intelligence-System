from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException

from api.schemas import ETLRequest, ETLResponse
from etl.pipeline import run

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/etl", tags=["etl"])


def _run_etl_task(full_reload: bool, tables: list[str] | None) -> None:
    try:
        results = run(tables=tables, full_reload=full_reload)
        logger.info("ETL task finished: %s", results)
    except Exception:
        logger.exception("ETL task failed")


@router.post("/run", response_model=ETLResponse)
async def trigger_etl(request: ETLRequest, background_tasks: BackgroundTasks) -> ETLResponse:
    background_tasks.add_task(_run_etl_task, request.full_reload, request.tables)
    return ETLResponse(message="ETL task started in background")
