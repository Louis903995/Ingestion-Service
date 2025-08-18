from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List


class LigneTicketInterpretee(BaseModel):
    taux_tva: Optional[int] = None
    libelle_produit: Optional[str] = None
    qte: int = 1
    categorie_produit_id: Optional[int] = None
    pu: Optional[float] = None
    montant: Optional[float] = None


class TicketInterprete(BaseModel):
    nom_enseigne: Optional[str] = None
    enseigne_id: Optional[int] = None
    tel_enseigne: Optional[str] = None
    date_heure_ticket: Optional[datetime] = None
    montant_total_ticket: Optional[float] = None
    lignes: List[LigneTicketInterpretee] = []
