from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List


class LigneTicketScanne(BaseModel):
    taux_tva: Optional[int]
    libelle_produit: Optional[str]
    qte: Optional[int]
    pu: Optional[float]
    montant: Optional[float]


class TicketScanne(BaseModel):
    nom_enseigne: Optional[str]
    tel_enseigne: Optional[str]
    date_heure_ticket: Optional[datetime]
    montant_total_ticket: Optional[float]
    lignes: List[LigneTicketScanne]
