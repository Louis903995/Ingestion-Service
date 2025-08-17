from typing import Optional
from sqlmodel import Field, SQLModel


class ProduitCategorie(SQLModel, table=True):
    categorie_produit_id: Optional[int] = Field(default=None, primary_key=True)
    nom_categorie_produit: str

    __tablename__ = "ProduitCategories"
    __table_args__ = {"schema": "achats"}

ProduitCategorie.model_rebuild()    
