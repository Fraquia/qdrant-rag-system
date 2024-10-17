from __future__ import annotations
from pydantic import BaseModel, Field


class NonHealthResponse(BaseModel):
    status: int = Field(..., example=500, description="The status code")

    description: str = Field(
        ...,
        example="Error",
        description="Any description regarding the status code of an error",
    )