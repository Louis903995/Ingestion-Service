import Levenshtein
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.enseigne import Enseigne, EnseigneCreate, EnseigneUpdate


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

    @staticmethod
    def get_enseignes_dict(session: Session) -> dict[int, tuple[str, str]]:
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

    @staticmethod
    def trouve_enseigne_id(
        enseignes: dict[int, tuple[str, str]],
        nom_enseigne_ticket: str,
        num_tel_enseigne_ticket: str | None = None,
        seuil_score_global: float = 0.80,
        poids_nom: float = 0.8,
        poids_tel: float = 0.2,
    ) -> int | None:
        best_score = -1
        best_id = None
        for k, (nom, tel) in enseignes.items():
            score_nom = Levenshtein.ratio(nom.lower(), nom_enseigne_ticket.lower())
            if num_tel_enseigne_ticket:
                score_tel = Levenshtein.ratio(tel, num_tel_enseigne_ticket)
                score = poids_nom * score_nom + poids_tel * score_tel
            else:
                score = score_nom
            if score > best_score:
                best_score = score
                best_id = k
        return best_id if best_score >= seuil_score_global else None
