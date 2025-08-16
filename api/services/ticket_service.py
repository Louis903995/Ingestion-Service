from sqlmodel import Session, select, func
from api.models.ticket import (
    TicketEntete,
    TicketEnteteCreate,
    TicketLignes,
    TicketLignesCreate,
)
from api.models.produit_categorie import ProduitCategorie
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import selectinload

# Exemple de JSON d'entrée pour la création :
# {
#   "client_id": 1,
#   "date_heure_ticket": "2025-08-16T09:30:00",
#   "enseigne_id": 2,
#   "montant_total_ticket": 99.99,
#   "lignes": [
#       {
#           "libelle_produit": "Café",
#           "quantite": 1,
#           "categorie_produit_id": 3,
#           "prix_unitaire": 2.0,
#           "montant_total_ligne": 2
#       },
#       {
#           "libelle_produit": "Croissant",
#           "quantite": 2,
#           "categorie_produit_id": 4,
#           "prix_unitaire": 1.5,
#           "montant_total_ligne": 3
#       }
#   ]
# }


class TicketService:

    @staticmethod
    def create_ticket_with_lignes(
        session: Session, ticket_data: Dict[str, Any]
    ) -> TicketEntete:
        lignes_data = ticket_data.pop("lignes", [])
        ticket_entete = TicketEnteteCreate(**ticket_data)
        db_ticket = TicketEntete.model_validate(ticket_entete)
        session.add(db_ticket)
        session.commit()
        session.refresh(db_ticket)

        db_lignes = []
        for ligne in lignes_data:
            db_ligne = TicketLignesCreate(ticket_id=db_ticket.ticket_id, **ligne)
            db_ligne_db = TicketLignes.model_validate(db_ligne)
            session.add(db_ligne_db)
            db_lignes.append(db_ligne_db)
        session.commit()

        for l in db_lignes:
            session.refresh(l)

        return db_ticket

    @staticmethod
    def get_tickets_with_lignes_and_categorie_nom(
        session: Session,
        client_id: int,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
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
            ticket_dict = {
                "ticket_id": ticket.ticket_id,
                "client_id": ticket.client_id,
                "date_heure_ticket": ticket.date_heure_ticket.isoformat(),
                "enseigne_id": ticket.enseigne_id,
                "montant_total_ticket": ticket.montant_total_ticket,
                "lignes": [
                    {
                        "ticket_ligne_id": getattr(ligne, "ticket_ligne_id", None),
                        "libelle_produit": ligne.libelle_produit,
                        "quantite": ligne.quantite,
                        "categorie_produit_id": ligne.categorie_produit_id,
                        "nom_categorie_produit": ligne.nom_categorie_produit,
                        "prix_unitaire": ligne.prix_unitaire,
                        "montant_total_ligne": ligne.montant_total_ligne,
                    }
                    for ligne in lignes
                ],
            }
            results.append(ticket_dict)
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


# # Exemple d'utilisation
# if __name__ == "__main__":
#     from api.db import engine  # Adapte ce chemin selon ton projet

#     # Exemple d'insertion
#     ticket_json = {
#         "client_id": 1,
#         "date_heure_ticket": "2025-08-16T09:30:00",
#         "enseigne_id": 2,
#         "montant_total_ticket": 99.99,
#         "lignes": [
#             {
#                 "libelle_produit": "Café",
#                 "quantite": 1,
#                 "categorie_produit_id": 3,
#                 "prix_unitaire": 2.0,
#                 "montant_total_ligne": 2,
#             },
#             {
#                 "libelle_produit": "Croissant",
#                 "quantite": 2,
#                 "categorie_produit_id": 4,
#                 "prix_unitaire": 1.5,
#                 "montant_total_ligne": 3,
#             },
#         ],
#     }
#     with Session(engine) as session:
#         ticket = create_ticket_with_lignes(session, ticket_json)
#         print(f"Ticket créé, id: {ticket.ticket_id}")

#         # Lecture avec les noms de catégories
#         result = get_ticket_with_lignes_and_categorie_nom(session, ticket.ticket_id)
#         from pprint import pprint

#         pprint(result)
