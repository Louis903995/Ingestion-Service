from sqlmodel import SQLModel
from typing import Optional

# Modèle pour mise à jour 
class ClientUpdate(SQLModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    budget: Optional[float] = None

# Créer un client en ne specifiant que le nom, prenom et le budget 
class ClientCreate(SQLModel):
    nom: str
    prenom: str
    budget: float