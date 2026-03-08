from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    collection_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    k: int = Field(default=10, ge=1, le=100)
    metadata: Optional[dict] = None
    session_id: Optional[str] = None
    history: List[List[str]] = []
