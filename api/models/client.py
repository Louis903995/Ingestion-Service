from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom_client: str = Field(max_length=100)
    prenom_client: str = Field(max_length=100)
    email_client: Optional[str] = Field(default=None, max_length=100, unique=True)
    adresse_client: Optional[str] = Field(default=None, max_length=100, unique=True)
    budget_client: float = Field(default=0.0)
    date_creation: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    date_modification: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
