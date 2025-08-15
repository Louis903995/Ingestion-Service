from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.enseigne import Client


class EnseigneService:

    @staticmethod
    def get_all_enseigne(session: Session):
        return session.exec(select(Client)).all()

    @staticmethod
    def get_enseigne_by_id(session: Session, enseigne_id: int):
        enseigne = session.get(Client, enseigne_id)
        if not enseigne:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        return enseigne

    # @staticmethod
    # def create_enseigne(session: Session, enseigne_create: ClientCreate):
    #     raise NotImplementedError("Cette méthode n'est pas encore implémentée.")

    # @staticmethod
    # def update_enseigne(
    #     session: Session, enseigne_id: int, enseigne_update: ClientUpdate
    # ):
    #     raise NotImplementedError("Cette méthode n'est pas encore implémentée.")

    @staticmethod
    def delete_enseigne(session: Session, enseigne_id: int):
        raise NotImplementedError("Cette méthode n'est pas encore implémentée.")
