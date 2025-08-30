from typing import List
from pydantic import BaseModel

class NumbersResponse(BaseModel):
    list_a: List[float]
    list_b: List[float]
