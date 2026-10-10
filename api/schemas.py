"""Pydantic request/response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Table_name = Literal[
    "geolocation",
    "customers",
    "sellers",
    "products",
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
]


class HealthResponse(BaseModel):
    status: Literal["healthy"] = "healthy"
    generator_ready: bool = False


class ETLRequest(BaseModel):
    full_reload: bool = Field(default=False, description="Truncate tables first (postgres backend only).")
    tables: list[Table_name] | None = Field(
        default=None, description="Restrict the load to these tables; default is all eight."
    )


class ETLResponse(BaseModel):
    message: str
    detail: dict[str, int] | None = None


class OrderGenRequest(BaseModel):
    count: int = Field(default=10, ge=1, le=10_000, description="Number of synthetic orders.")


class OrderGenResponse(BaseModel):
    message: str
