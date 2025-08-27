from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Client(BaseModel):
    nom_client: str
    prenom_client: str
    email_client: str
    adresse_client: Optional[str] = None
    budget_client: float = 0


class ClientResponse(Client):
    client_id: int
    date_creation: datetime
    date_modification: datetime
