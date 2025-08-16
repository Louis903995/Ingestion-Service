from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, Session, select
from datetime import datetime
from pydantic import BaseModel


class TicketEnteteBase(SQLModel):
    client_id: int
    date_heure_ticket: datetime
    enseigne_id: int
    montant_total_ticket: float


class TicketEntete(TicketEnteteBase, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    lignes: List["TicketLignes"] = Relationship(back_populates="ticket")

    __tablename__ = "TicketEntetes"
    __table_args__ = {"schema": "achats"}


class TicketEnteteCreate(TicketEnteteBase):
    pass

    """
    Cette classe ne doit jamais être utilisée : les entêtes de ticket ne sont jamais modifiés.
    """


class TicketEnteteUpdate(TicketEnteteBase):
    pass
    """
    Cette classe ne doit jamais être utilisée : les ticket ne sont jamais modifiés.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError(
            "TicketEnteteUpdate ne doit jamais être instanciée (entêtes non modifiables)"
        )


class TicketLignesBase(SQLModel):
    ticket_id: int
    libelle_produit: str
    quantite: int = 1
    categorie_produit_id: Optional[int]
    prix_unitaire: Optional[float] = None
    montant_total_ligne: int


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.models.produit_categorie import ProduitCategorie


class TicketLignes(TicketLignesBase, table=True):
    ticket_ligne_id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="achats.TicketEntetes.ticket_id")
    categorie_produit_id: Optional[int] = Field(
        default=None, foreign_key="achats.ProduitCategories.categorie_produit_id"
    )
    ticket: Optional["TicketEntete"] = Relationship(back_populates="lignes")
    categorie: Optional["ProduitCategorie"] = Relationship(
        sa_relationship_kwargs={"lazy": "joined"}
    )
    __tablename__ = "TicketLignes"
    __table_args__ = {"schema": "achats"}

    @property
    def nom_categorie_produit(self) -> Optional[str]:
        if self.categorie is not None:
            return self.categorie.nom_categorie_produit
        return None


class TicketLignesCreate(TicketLignesBase):
    pass


class TicketLignesUpdate(TicketLignesBase):
    pass

    """
    Cette classe ne doit jamais être utilisée : les lignes de ticket ne sont jamais modifiés.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError(
            "TicketLignesUpdate ne doit jamais être instanciée (lignes non modifiables)"
        )


TicketLignes.model_rebuild()


class TicketLigneResponse(BaseModel):
    ticket_ligne_id: Optional[int]
    libelle_produit: str
    quantite: int
    categorie_produit_id: Optional[int]
    nom_categorie_produit: Optional[str]
    prix_unitaire: Optional[float]
    montant_total_ligne: Optional[float]


class TicketEnteteResponse(BaseModel):
    ticket_id: int
    client_id: int
    date_heure_ticket: str  # ou datetime selon ton besoin
    enseigne_id: int
    montant_total_ticket: float
    lignes: List[TicketLigneResponse]
