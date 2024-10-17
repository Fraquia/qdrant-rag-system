from pydantic import BaseModel
from typing import Optional


class Metadata(BaseModel):
    knowledge_box: Optional[str]    # project id
    title: Optional[str]
    property: Optional[str]
    weight: Optional[float]
    length: Optional[float]
    price: Optional[float]
    delivery_time: Optional[str]
    discount: Optional[float]
    supplier: Optional[str]
