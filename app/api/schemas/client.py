from sqlmodel import SQLModel
from typing import Optional

# Modèle pour mise à jour 
class ClientUpdate(SQLModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None
    adresse: Optional[str] = None
    budget: Optional[float] = None


# Créer un client en ne specifiant que le nom, prenom et le budget
# L'email et l'adresse sont optionnels 
class ClientCreate(SQLModel):
    nom: str
    prenom: str
    email: Optional[str] = None
    adresse: Optional[str] = None
    budget: float