from __future__ import annotations

from fastapi import APIRouter, Request

from api.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    return HealthResponse(generator_ready=request.app.state.generator_ready)
