from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    budget: float
    date_enregistrement: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)