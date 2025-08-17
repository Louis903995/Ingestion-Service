from sqlmodel import Session, select, func
from app.models.ticket import (
    TicketEntete,
    TicketEnteteCreate,
    TicketLignes,
    TicketLignesCreate,
)
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import selectinload
from app.schemas.ticket_reponse import TicketEnteteResponse, TicketLigneResponse
from reconnaissance_tickets.model_ticket import TicketInterprete


class TicketService:

    @staticmethod
    def create_ticket(
        session: Session,
        user_id: int,
        ticket_scanne: TicketInterprete,
    ) -> TicketEntete | None:
        try:

            # Création de l'entête du ticket
            ticket_entete = TicketEnteteCreate(
                client_id=user_id,
                enseigne_id=ticket_scanne.enseigne_id,
                date_heure_ticket=ticket_scanne.date_heure_ticket,
                montant_total_ticket=ticket_scanne.montant_total_ticket,
            )
            db_ticket = TicketEntete.model_validate(ticket_entete)
            session.add(db_ticket)
            session.commit()
            session.refresh(db_ticket)

            db_lignes = []
            for ligne in ticket_scanne.lignes:
                ligne_create = TicketLignesCreate(
                    ticket_id=db_ticket.ticket_id,
                    libelle_produit=ligne.libelle_produit,
                    quantite=ligne.qte,
                    categorie_produit_id=ligne.categorie_produit_id,
                    prix_unitaire=ligne.pu,
                    montant_total_ligne=ligne.montant,
                )
                db_ligne_db = TicketLignes.model_validate(ligne_create)
                session.add(db_ligne_db)
                db_lignes.append(db_ligne_db)
            session.commit()

            for l in db_lignes:
                session.refresh(l)

            return db_ticket
        except Exception as e:
            pass
        # logger !
        return None

    @staticmethod
    def get_tickets(
        session: Session,
        client_id: int,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None,
    ) -> List[TicketEnteteResponse]:
        # Filtre obligatoire sur client_id
        statement = select(TicketEntete).where(TicketEntete.client_id == client_id)
        if date_debut is not None:
            statement = statement.where(TicketEntete.date_heure_ticket >= date_debut)
        if date_fin is not None:
            statement = statement.where(TicketEntete.date_heure_ticket <= date_fin)

        tickets = session.exec(statement).all()
        results = []

        for ticket in tickets:
            lignes_statement = (
                select(TicketLignes)
                .options(selectinload(TicketLignes.categorie))
                .where(TicketLignes.ticket_id == ticket.ticket_id)
            )
            lignes = session.exec(lignes_statement).all()
            ticket_response = TicketEnteteResponse(
                ticket_id=ticket.ticket_id,
                client_id=ticket.client_id,
                date_heure_ticket=ticket.date_heure_ticket.isoformat(),
                enseigne_id=ticket.enseigne_id,
                montant_total_ticket=ticket.montant_total_ticket,
                lignes=[
                    TicketLigneResponse(
                        ticket_ligne_id=getattr(ligne, "ticket_ligne_id", None),
                        libelle_produit=ligne.libelle_produit,
                        quantite=ligne.quantite,
                        categorie_produit_id=ligne.categorie_produit_id,
                        nom_categorie_produit=ligne.nom_categorie_produit,
                        prix_unitaire=ligne.prix_unitaire,
                        montant_total_ligne=ligne.montant_total_ligne,
                    )
                    for ligne in lignes
                ],
            )
            results.append(ticket_response)
        return results

    @staticmethod
    def get_montant_total_par_categorie(
        session: Session,
        client_id: int,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None,
        categorie_id: Optional[int] = None,
    ) -> float:
        # On sélectionne les entêtes de ticket du client sur la période
        ticket_stmt = select(TicketEntete.ticket_id).where(
            TicketEntete.client_id == client_id
        )
        if date_debut is not None:
            ticket_stmt = ticket_stmt.where(
                TicketEntete.date_heure_ticket >= date_debut
            )
        if date_fin is not None:
            ticket_stmt = ticket_stmt.where(TicketEntete.date_heure_ticket <= date_fin)
        ticket_ids = ticket_ids = [row for row in session.exec(ticket_stmt).all()]
        if not ticket_ids:
            return 0.0

        # On filtre les lignes de ticket correspondant aux tickets trouvés
        ligne_stmt = select(func.sum(TicketLignes.montant_total_ligne))
        ligne_stmt = ligne_stmt.where(TicketLignes.ticket_id.in_(ticket_ids))
        if categorie_id is not None:
            ligne_stmt = ligne_stmt.where(
                TicketLignes.categorie_produit_id == categorie_id
            )

        montant_total = session.exec(ligne_stmt).one()
        return montant_total or 0.0
