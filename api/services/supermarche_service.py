from sqlmodel import Session, select
from fastapi import HTTPException
from models.supermarche import Supermarche

class SupermarcheService:
    
    @staticmethod
    def get_all_supermarches(session: Session):
        return session.exec(select(Supermarche)).all()
    
    @staticmethod
    def get_supermarche_by_id(session: Session, supermarche_id: int):
        supermarche = session.get(Supermarche, supermarche_id)
        if not supermarche:
            raise HTTPException(status_code=404, detail="Supermarché non trouvé")
        return supermarche
    
    @staticmethod
    def create_supermarche(session: Session, supermarche: Supermarche):
        session.add(supermarche)
        session.commit()
        session.refresh(supermarche)
        return supermarche
    
    @staticmethod
    def update_supermarche(session: Session, supermarche_id: int, supermarche_update: Supermarche):
        db_supermarche = session.get(Supermarche, supermarche_id)
        if not db_supermarche:
            raise HTTPException(status_code=404, detail="Supermarché non trouvé")

        for key, value in supermarche_update.dict(exclude_unset=True).items():
            setattr(db_supermarche, key, value)

        session.add(db_supermarche)
        session.commit()
        session.refresh(db_supermarche)
        return db_supermarche
    
    @staticmethod
    def delete_supermarche(session: Session, supermarche_id: int):
        db_supermarche = session.get(Supermarche, supermarche_id)
        if not db_supermarche:
            raise HTTPException(status_code=404, detail="Supermarché non trouvé")

        session.delete(db_supermarche)
        session.commit()
        return {"message": "Supermarché supprimé avec succès"}