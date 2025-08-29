from pydantic import BaseModel
from typing import List

class DataResponse(BaseModel):
    valeurs_passees: List[int]
    valeur_actuelle: int
