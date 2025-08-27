from sqlmodel import SQLModel, Field
from typing import Optional
import datetime


# Modèle pour mise à jour
class ClientUpdate(SQLModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None
    adresse: Optional[str] = None
    budget: Optional[float] = None


# Créer un client en ne specifiant que le nom, prenom et le budget
# L'email et l'adresse sont optionnels
class ClientCreate(SQLModel):
    nom: str
    prenom: str
    email: str
    adresse: str
    budget: float


class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom_client: str = Field(max_length=100)
    prenom_client: str = Field(max_length=100)
    email_client: str = Field(default=None, max_length=100, unique=True)
    adresse_client: str = Field(default=None, max_length=100, unique=True)
    budget_client: float = Field(default=0.0)
    date_creation: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.utcnow
    )
    date_modification: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.utcnow
    )

    __tablename__ = "Clients"
    __table_args__ = {"schema": "clients"}
