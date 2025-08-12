from sqlmodel import Session, select
from fastapi import HTTPException
from models.categorie import Categorie

class CategorieService:
    
    @staticmethod
    def get_all_categories(session: Session):
        return session.exec(select(Categorie)).all()
    
    @staticmethod
    def get_category_by_id(session: Session, categorie_id: int):
        category = session.get(Categorie, categorie_id)
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")
        return category
    
    @staticmethod
    def create_category(session: Session, category: Categorie):
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
    @staticmethod
    def update_category(session: Session, categorie_id: int, category_update: Categorie):
        db_category = session.get(Categorie, categorie_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")

        for key, value in category_update.dict(exclude_unset=True).items():
            setattr(db_category, key, value)

        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category
    
    @staticmethod
    def delete_category(session: Session, categorie_id: int):
        db_category = session.get(Categorie, categorie_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")

        session.delete(db_category)
        session.commit()
        return {"message": "Catégorie supprimée avec succès"}