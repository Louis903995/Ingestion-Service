import copy
import logging
import pytest
from datetime import timedelta
from reconnaissance_tickets.model_ticket import TicketInterprete
from api.services.ticket_service import TicketService
from tests.database.pyodbc_tickets_utils import insere_ticket
from tests.pyodbc_utils import execute_script_sql
from tests.database.conftest import (
    # session,  # surtout ne pas oublier
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


def test_get_tickets(session, simple_ticket_interprete):
    # on veut 3 copies différentes, pas 3 références sur le même objet
    ticket_interprete_1 = copy.deepcopy(simple_ticket_interprete)

    ticket_interprete_2 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_2.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket - timedelta(days=2)
    )  # 2 jours avant

    ticket_interprete_3 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_3.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket + timedelta(days=2)
    )  # 2 jours après
    user_id = 1

    insere_ticket(ticket_interprete_1, user_id)
    insere_ticket(ticket_interprete_2, user_id)
    insere_ticket(ticket_interprete_3, user_id)

    tickets = TicketService.get_tickets(session, client_id=user_id)
    assert len(tickets) == 3
    print(tickets)
