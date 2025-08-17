import logging
import pyodbc

from app.schemas.ticket_interprete import TicketInterprete
from tests.database.conftest import PYODBC_CONNECTION_STRING, DB_NAME_TEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def insere_ticket(ticket: TicketInterprete, client_id: int) -> bool:
    try:
        with pyodbc.connect(PYODBC_CONNECTION_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO [{DB_NAME_TEST}].[achats].[TicketEntetes] (client_id, date_heure_ticket, enseigne_id, montant_total_ticket)
                OUTPUT INSERTED.ticket_id
                VALUES (?, ?, ?, ?)
            """,
                (
                    client_id,
                    ticket.date_heure_ticket,
                    ticket.enseigne_id,
                    ticket.montant_total_ticket,
                ),
            )
            # Récupérer le ticket_id généré
            ticket_id = cursor.fetchone()[0]

            # Insérer les lignes
            for ligne in ticket.lignes:
                cursor.execute(
                    f"""
                    INSERT INTO [{DB_NAME_TEST}].[achats].[TicketLignes] (
                        ticket_id, libelle_produit, quantite, categorie_produit_id,
                        prix_unitaire, montant_total_ligne
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        ticket_id,
                        ligne.libelle_produit,
                        ligne.qte,
                        ligne.categorie_produit_id,
                        ligne.pu,
                        ligne.montant,
                    ),
                )
            conn.commit()
            return True
    except Exception as e:
        logger.critical(e)
        return False
