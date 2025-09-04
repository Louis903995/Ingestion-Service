from decimal import Decimal
import logging
import pytest
from datetime import datetime
import pyodbc
from app.config import get_db_name
from app.schemas.ticket_interprete import TicketInterprete
from app.services.ticket_service import TicketService
from tests.database.conftest import PYODBC_CONNECTION_STRING


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def simple_ticket_interprete():
    return TicketInterprete.model_validate_json(
        """{
        "nom_enseigne": "MARKET BAISIEUX",
        "tel_enseigne": "03 20 41 94 28",
        "date_heure_ticket": "2025-07-03T16:47:52",
        "montant_total_ticket": 35.55,
        "enseigne_id": 1,
        "lignes": [
            {
                "taux_tva": 7,
                "libelle_produit": "*100G NENTOS FESH H",
                "qte": 4,
                "pu": 3.54,
                "montant": 14.16,
                "categorie_produit_id": 1
            },
            {
                "taux_tva": 6,
                "libelle_produit": "*606G SORB CIT MX",
                "qte": 1,
                "pu": null,
                "montant": 2.29,
                "categorie_produit_id": 2
            },
            {
                "taux_tva": 6,
                "libelle_produit": "*650G BAC POMME CHF",
                "qte": 2,
                "pu": 9.55,
                "montant": 19.1,
                "categorie_produit_id": 2
            }
        ]
}"""
    )


def test_create_ticket(session, simple_ticket_interprete):
    user_id = 42
    ticket = TicketService.create_ticket(session, user_id, simple_ticket_interprete)
    ticket_id = ticket.ticket_id
    attendu = [
        (
            ticket_id,
            user_id,
            datetime(2025, 7, 3, 16, 47, 52),
            1,
            Decimal("35.55"),
            "*100G NENTOS FESH H",
            4,
            1,
            Decimal("3.54"),
            Decimal("14.16"),
        ),
        (
            ticket_id,
            user_id,
            datetime(2025, 7, 3, 16, 47, 52),
            1,
            Decimal("35.55"),
            "*606G SORB CIT MX",
            1,
            2,
            None,
            Decimal("2.29"),
        ),
        (
            ticket_id,
            user_id,
            datetime(2025, 7, 3, 16, 47, 52),
            1,
            Decimal("35.55"),
            "*650G BAC POMME CHF",
            2,
            2,
            Decimal("9.55"),
            Decimal("19.10"),
        ),
    ]
    try:
        with pyodbc.connect(PYODBC_CONNECTION_STRING) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT
                    te.ticket_id,
                    te.client_id,
                    te.date_heure_ticket,
                    te.enseigne_id,
                    te.montant_total_ticket,
                    tl.libelle_produit,
                    tl.quantite,
                    tl.categorie_produit_id,
                    tl.prix_unitaire,
                    tl.montant_total_ligne
                FROM [{get_db_name()}].[achats].[TicketEntetes] AS te
                INNER JOIN [{get_db_name()}].[achats].[TicketLignes] AS tl
                    ON te.ticket_id = tl.ticket_id
                WHERE te.ticket_id = {ticket_id}
                ORDER BY te.ticket_id, tl.ticket_ligne_id
                """
            cursor.execute(query)
            resultat = [tuple(row) for row in cursor.fetchall()]
            assert list(resultat) == attendu
    except AssertionError:
        raise
    except Exception as e:
        logger.critical(e)
        raise
