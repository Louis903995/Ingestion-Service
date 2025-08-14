from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=100)
    prenom: str = Field(max_length=100)
    email: Optional[str] = Field(default=None, max_length=100, unique=True)
    adresse: Optional[str] = Field(default=None, max_length=100, unique=True)
    budget: float = Field(default=0.0)
    date_enregistrement: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    date_derniere_modification: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
