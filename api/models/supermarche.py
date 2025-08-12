from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Supermarche(SQLModel, table=True):
    id_supermarche: Optional[int] = Field(default=None, primary_key=True)
    id_ticket: int = Field(foreign_key="ticket.id_ticket")
    nom_magasin: str
    date_achat: datetime.date
    prix_total: float