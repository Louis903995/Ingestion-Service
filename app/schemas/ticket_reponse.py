from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List


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
    date_heure_ticket: datetime
    enseigne_id: int
    montant_total_ticket: float
    lignes: List[TicketLigneResponse]
