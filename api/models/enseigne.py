from sqlmodel import SQLModel, Field
from typing import Optional


class Client(SQLModel, table=True):
    enseigne_id: Optional[int] = Field(default=None, primary_key=True)
    enseigne_nom: str = Field(max_length=100)
    enseigne_adresse: str = Field(max_length=100)
    enseigne_numero_tel: str = Field(max_length=100)
    taille_enseigne_id: int


from sqlmodel import Field, Relationship, SQLModel, Session
from typing import Optional


class EnseigneTaille(SQLModel, table=True):
    taille_enseigne_id: Optional[int] = Field(default=None, primary_key=True)
    libelle_taille_enseigne: str


class Enseigne(SQLModel, table=True):
    enseigne_id: Optional[int] = Field(default=None, primary_key=True)
    enseigne_nom: str = Field(max_length=100)
    enseigne_adresse: str = Field(max_length=100)
    enseigne_numero_tel: str = Field(max_length=100)
    taille_enseigne_id: Optional[int] = Field(
        default=None, foreign_key="enseignetaille.taille_enseigne_id"
    )
    taille: Optional[EnseigneTaille] = Relationship(back_populates="enseignes")


def get_enseigne_with_taille(session: Session, enseigne_id: int):
    enseigne = session.get(Enseigne, enseigne_id)
    if enseigne:
        print(
            f"Taille: {enseigne.taille.libelle_taille_enseigne}"
        )  # Accès au libellé via la relation
    return enseigne
