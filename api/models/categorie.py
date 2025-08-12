from sqlmodel import SQLModel, Field
from typing import Optional

class Categorie(SQLModel, table=True): #2 colonnes 
    id_cat: Optional[int] = Field(default=None, primary_key=True)
    id_ticket: int = Field(foreign_key="ticket.id_ticket")
    libelle: str
    categorie: str

