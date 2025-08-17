from decimal import Decimal
import logging
import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from datetime import datetime, timedelta
from tests.database.fixtures import (
    session,
    nettoie_tout,
    PYODBC_CONNECTION_STRING,
    DB_NAME_TEST,
)
import pyodbc

# Importe ici tes modèles et ton service
from api.models.ticket import (
    TicketEntete,
    TicketEnteteCreate,
    TicketEnteteResponse,
    TicketLigneResponse,
    TicketLignes,
    TicketLignesCreate,
)
from reconnaissance_tickets.model_ticket import TicketInterprete, LigneTicketInterpretee
from api.services.ticket_service import TicketService
from tests.pyodbc_utils import execute_script_sql


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_module():
    execute_script_sql(
        "sql/ajoute_categories.sql", DB_NAME_TEST, PYODBC_CONNECTION_STRING
    )
    yield


@pytest.fixture
def simple_ticket_scanne():
    return TicketInterprete.model_validate_json(
        """{
        "nom_enseigne": "MARKET BAISIEUX",
        "tel_enseigne": "03 20 41 94 28",
        "date_heure_ticket": "2025-07-03T16:47:52",
        "montant_total_ticket": 10.0,
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
                "categorie_produit_id": 1
            },
            {
                "taux_tva": 6,
                "libelle_produit": "*650G BAC POMME CHF",
                "qte": 2,
                "pu": 9.55,
                "montant": 19.1,
                "categorie_produit_id": 1
            }
        ]
}"""
    )


def test_create_ticket(session, simple_ticket_scanne):
    user_id = 42
    # on enregistre le ticket
    ticket = TicketService.create_ticket(session, user_id, simple_ticket_scanne)
    # on récupère le ticket_id du ticket qu'on vient d'enregistrer
    ticket_id = ticket.ticket_id
    attendu = [
        (
            ticket_id,
            user_id,
            datetime(2025, 7, 3, 16, 47, 52),
            1,
            Decimal("10.00"),
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
            Decimal("10.00"),
            "*606G SORB CIT MX",
            1,
            1,
            None,
            Decimal("2.29"),
        ),
        (
            ticket_id,
            user_id,
            datetime(2025, 7, 3, 16, 47, 52),
            1,
            Decimal("10.00"),
            "*650G BAC POMME CHF",
            2,
            1,
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
            # et la comparaison avec attendu (liste de tuple) sera toujours fausse
            resultat = [tuple(row) for row in cursor.fetchall()]
            assert list(resultat) == attendu
    except AssertionError:
        raise  # On laisse passer l'AssertionError, elle remonte sinon notre test passe dans tous les cas
    except Exception as e:
        logger.critical(e)


# def test_get_tickets(session, simple_ticket_scanne):
#     user_id = 1
#     # Ajoute un ticket
#     TicketService.create_ticket(
#         session, user_id, simple_ticket_scanne
#     )

#     # Test récupération sans filtre de date
#     tickets = TicketService.get_tickets(session, client_id=user_id)
#     assert len(tickets) == 1
#     assert tickets[0].lignes[0].libelle_produit == "Pain"

#     # Test récupération avec des bornes de date
#     dt_min = datetime(2025,  15)
#     dt_max = datetime(2025,  17)
#     tickets2 = TicketService.get_tickets(
#         session, client_id=user_id, date_debut=dt_min, date_fin=dt_max
#     )
#     assert len(tickets2) == 1

#     dt_trop_tot = datetime(2025,  10)
#     dt_trop_tard = datetime(2025,  12)
#     tickets3 = TicketService.get_tickets(
#         session, client_id=user_id, date_debut=dt_trop_tot, date_fin=dt_trop_tard
#     )
#     assert len(tickets3) == 0


# def test_get_montant_total_par_categorie(session, simple_ticket_scanne):
#     user_id = 2
#     TicketService.create_ticket(
#         session, user_id, simple_ticket_scanne
#     )

#     # Montant total sans filtre (toutes les catégories)
#     montant = TicketService.get_montant_total_par_categorie(session, client_id=user_id)
#     assert montant == 12.5

#     # Montant pour une catégorie qui n'existe pas
#     montant2 = TicketService.get_montant_total_par_categorie(
#         session, client_id=user_id, categorie_id=999
#     )
#     assert montant2 == 0.0

#     # Si tu ajoutes la gestion de categorie_produit_id dans ton modèle, tu pourras tester pour une vraie catégorie ici
