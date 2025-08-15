from sqlmodel import Session, select
from fastapi import HTTPException

from api.models.enseigne import Enseigne, EnseigneCreate, EnseigneUpdate


class EnseigneService:

    @staticmethod
    def get_all_enseignes(session: Session):
        return session.exec(select(Enseigne)).all()

    @staticmethod
    def get_enseigne_by_id(session: Session, enseigne_id: int):
        enseigne = session.get(Enseigne, enseigne_id)
        if not enseigne:
            raise HTTPException(status_code=404, detail="Enseigne non trouvée")
        return enseigne

    @staticmethod
    def create_enseigne(session: Session, enseigne_create: EnseigneCreate):
        raise NotImplementedError("Cette méthode n'est pas encore implémentée.")

    @staticmethod
    def update_enseigne(
        session: Session, enseigne_id: int, enseigne_update: EnseigneUpdate
    ):
        raise NotImplementedError("Cette méthode n'est pas encore implémentée.")

    @staticmethod
    def delete_enseigne(session: Session, enseigne_id: int):
        raise NotImplementedError("Cette méthode n'est pas encore implémentée.")

    def get_enseignes_dict(session: Session):
        statement = select(
            Enseigne.enseigne_id,
            Enseigne.enseigne_nom_ticket,
            Enseigne.enseigne_num_tel_ticket,
        )
        results = session.exec(statement)
        return {
            enseigne_id: (enseigne_nom_ticket, enseigne_num_tel_ticket)
            for enseigne_id, enseigne_nom_ticket, enseigne_num_tel_ticket in results
        }
