from decimal import Decimal
import logging
import pytest
from datetime import datetime
import pyodbc
from reconnaissance_tickets.model_ticket import TicketInterprete, LigneTicketInterpretee
from app.services.ticket_service import TicketService
from tests.pyodbc_utils import execute_script_sql
from tests.database.conftest import (
    session,  # surtout ne pas oublier
    PYODBC_CONNECTION_STRING,
    DB_NAME_TEST,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_module():
    execute_script_sql(
        "sql/ajoute_categories.sql", DB_NAME_TEST, PYODBC_CONNECTION_STRING
    )
    yield


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
    # on enregistre le ticket
    ticket = TicketService.create_ticket(session, user_id, simple_ticket_interprete)
    # on récupère le ticket_id du ticket qu'on vient d'enregistrer
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
                FROM [{DB_NAME_TEST}].[achats].[TicketEntetes] AS te
                INNER JOIN [{DB_NAME_TEST}].[achats].[TicketLignes] AS tl
                    ON te.ticket_id = tl.ticket_id
                WHERE te.ticket_id = {ticket_id}
                ORDER BY te.ticket_id, tl.ticket_ligne_id
                """
            cursor.execute(query)
            # on force resultat comme une liste de tuple car sinon c'est un pydobc.row
            # et la comparaison avec attendu (liste de tuple) sera toujours fausse
            resultat = [tuple(row) for row in cursor.fetchall()]
            assert list(resultat) == attendu
    except AssertionError:
        raise  # On laisse passer l'AssertionError, elle remonte sinon notre test passe dans tous les cas
    except Exception as e:
        logger.critical(e)
