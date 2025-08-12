from sqlmodel import SQLModel, Field
from typing import Optional

class Ticket(SQLModel, table=True):
    id_ticket: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.client_id")
    libelle: str