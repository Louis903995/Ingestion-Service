from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.produit_categorie import ProduitCategorie


class ProduitCategorieService:
    @staticmethod
    def get_all_produit_categories(session: Session):
        return session.exec(select(ProduitCategorie)).all()

    @staticmethod
    def get_produit_categorie_by_id(session: Session, produit_categorie_id: int):
        produit_categorie = session.get(ProduitCategorie, produit_categorie_id)
        if not produit_categorie:
            raise HTTPException(status_code=404, detail="Categorie produit non trouvée")
        return produit_categorie

    @staticmethod
    def get_produit_categorie_dict(session: Session) -> dict[str:int]:
        statement = select(
            ProduitCategorie.categorie_produit_id,
            ProduitCategorie.nom_categorie_produit,
        )
        results = session.exec(statement)
        return {
            nom_categorie_produit: categorie_produit_id
            for categorie_produit_id, nom_categorie_produit in results
        }
