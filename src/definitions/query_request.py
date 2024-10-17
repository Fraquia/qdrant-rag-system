from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str
    collection_name: str
    k: int
    metadata: Optional[dict] = None
    history: List[List[str]] = []

