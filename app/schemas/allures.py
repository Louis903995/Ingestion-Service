from typing import List
from pydantic import BaseModel

class AlluresResponse(BaseModel):
    depense_constate: List[float]
    depense_predite: List[float]

    