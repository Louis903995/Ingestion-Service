from typing import Optional
from sqlmodel import SQLModel, Field


class EnseigneBase(SQLModel):
    enseigne_nom: str
    enseigne_adresse: str
    categorie_enseigne: str
    enseigne_surface_m2: int
    enseigne_num_tel_ticket: str
    enseigne_nom_ticket: str


class Enseigne(EnseigneBase, table=True):
    enseigne_id: Optional[int] = Field(default=None, primary_key=True)

    __tablename__ = "Enseignes"
    __table_args__ = {"schema": "achats"}


class EnseigneCreate(EnseigneBase):
    pass


class EnseigneUpdate(SQLModel):
    enseigne_nom: Optional[str] = None
    enseigne_adresse: Optional[str] = None
    enseigne_num_tel_ticket: Optional[str] = None
    categorie_enseigne: Optional[str] = None
    enseigne_nom_ticket: Optional[str] = None
