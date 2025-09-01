from typing import List
from pydantic import BaseModel
from datetime import datetime

class MesureTemporelle(BaseModel):
    d: datetime
    v: float

class AlluresResponse(BaseModel):
    depense_constate: List[MesureTemporelle]
    depense_predite: List[MesureTemporelle]

