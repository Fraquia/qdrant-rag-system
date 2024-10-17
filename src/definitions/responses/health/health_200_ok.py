from __future__ import annotations
from pydantic import BaseModel, Field


class HealthResponse200Ok(BaseModel):
    status: int = Field(..., example=200, description="The status code")

    description: str = Field(
        ...,
        example="Up and running",
        description="Any description regarding the status code",
    )