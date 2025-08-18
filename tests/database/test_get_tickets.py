import copy
import logging
import pytest
from datetime import timedelta
from app.schemas.ticket_interprete import TicketInterprete
from app.schemas.ticket_reponse import TicketEnteteResponse, TicketLigneResponse

from app.services.ticket_service import TicketService
from tests.database.pyodbc_tickets_utils import insere_ticket
from tests.pyodbc_utils import execute_script_sql
from tests.database.conftest import PYODBC_CONNECTION_STRING, DB_NAME


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_module():
    execute_script_sql("sql/ajoute_categories.sql", DB_NAME, PYODBC_CONNECTION_STRING)
    yield


@pytest.fixture
def simple_ticket_interprete() -> TicketInterprete:
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


# compare 2 TicketEnteteResponse en ignorant leur ticket_ligne_id
def compare_ignorant_ticket_ligne_id(
    ticket_entete_rep1: TicketEnteteResponse,
    ticket_entete_rep2: TicketEnteteResponse,
) -> bool:
    # fonction qui supprime les ticket_ligne_id
    def supprime_ticket_ligne_ids(ticket_entete_rep: TicketEnteteResponse):
        ticket = copy.deepcopy(ticket_entete_rep)
        for ligne in ticket["lignes"]:
            if "ticket_ligne_id" in ligne:
                del ligne["ticket_ligne_id"]
        return ticket

    dump1 = supprime_ticket_ligne_ids(ticket_entete_rep1.model_dump())
    dump2 = supprime_ticket_ligne_ids(ticket_entete_rep2.model_dump())
    return dump1 == dump2


def test_get_tickets(session, simple_ticket_interprete):
    client_id = 10
    insere_ticket(simple_ticket_interprete, client_id)
    tickets = TicketService.get_tickets(session, client_id=client_id)
    assert len(tickets) == 1
    assert compare_ignorant_ticket_ligne_id(
        tickets[0],
        TicketEnteteResponse(
            ticket_id=tickets[0].ticket_id,
            client_id=client_id,
            date_heure_ticket="2025-07-03T16:47:52",
            enseigne_id=1,
            montant_total_ticket=35.55,
            lignes=[
                TicketLigneResponse(
                    ticket_ligne_id=1,  # ignoré
                    libelle_produit="*100G NENTOS FESH H",
                    quantite=4,
                    categorie_produit_id=1,
                    nom_categorie_produit="Fruits & légumes",
                    prix_unitaire=3.54,
                    montant_total_ligne=14.16,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=2,  # ignoré
                    libelle_produit="*606G SORB CIT MX",
                    quantite=1,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=None,
                    montant_total_ligne=2.29,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=3,  # ignoré
                    libelle_produit="*650G BAC POMME CHF",
                    quantite=2,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=9.55,
                    montant_total_ligne=19.1,
                ),
            ],
        ),
    )


def test_get_tickets_a_partir_de(session, simple_ticket_interprete):
    # on veut 3 copies différentes, pas 3 références sur le même objet
    ticket_interprete_1 = copy.deepcopy(simple_ticket_interprete)

    ticket_interprete_2 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_2.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket + timedelta(days=2)
    )  # 2 jours après

    ticket_interprete_3 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_3.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket + timedelta(days=4)
    )  # 4 jours après

    client_id = 20

    insere_ticket(ticket_interprete_1, client_id)
    insere_ticket(ticket_interprete_2, client_id)
    insere_ticket(ticket_interprete_3, client_id)

    tickets = TicketService.get_tickets(
        session, client_id=client_id, date_debut=ticket_interprete_2.date_heure_ticket
    )
    assert len(tickets) == 2
    assert compare_ignorant_ticket_ligne_id(
        tickets[0],
        TicketEnteteResponse(
            ticket_id=tickets[0].ticket_id,
            client_id=client_id,
            date_heure_ticket=ticket_interprete_2.date_heure_ticket,  # date du 2 eme ticket
            enseigne_id=1,
            montant_total_ticket=35.55,
            lignes=[
                TicketLigneResponse(
                    ticket_ligne_id=1,  # ignoré
                    libelle_produit="*100G NENTOS FESH H",
                    quantite=4,
                    categorie_produit_id=1,
                    nom_categorie_produit="Fruits & légumes",
                    prix_unitaire=3.54,
                    montant_total_ligne=14.16,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=2,  # ignoré
                    libelle_produit="*606G SORB CIT MX",
                    quantite=1,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=None,
                    montant_total_ligne=2.29,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=3,  # ignoré
                    libelle_produit="*650G BAC POMME CHF",
                    quantite=2,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=9.55,
                    montant_total_ligne=19.1,
                ),
            ],
        ),
    )
    assert compare_ignorant_ticket_ligne_id(
        tickets[1],
        TicketEnteteResponse(
            ticket_id=tickets[1].ticket_id,
            client_id=client_id,
            date_heure_ticket=ticket_interprete_3.date_heure_ticket,  # date du 3 eme ticket
            enseigne_id=1,
            montant_total_ticket=35.55,
            lignes=[
                TicketLigneResponse(
                    ticket_ligne_id=1,  # ignoré
                    libelle_produit="*100G NENTOS FESH H",
                    quantite=4,
                    categorie_produit_id=1,
                    nom_categorie_produit="Fruits & légumes",
                    prix_unitaire=3.54,
                    montant_total_ligne=14.16,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=2,  # ignoré
                    libelle_produit="*606G SORB CIT MX",
                    quantite=1,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=None,
                    montant_total_ligne=2.29,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=3,  # ignoré
                    libelle_produit="*650G BAC POMME CHF",
                    quantite=2,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=9.55,
                    montant_total_ligne=19.1,
                ),
            ],
        ),
    )


def test_get_tickets_avant(session, simple_ticket_interprete):
    # on veut 3 copies différentes, pas 3 références sur le même objet
    ticket_interprete_1 = copy.deepcopy(simple_ticket_interprete)

    ticket_interprete_2 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_2.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket + timedelta(days=2)
    )  # 2 jours après

    ticket_interprete_3 = copy.deepcopy(simple_ticket_interprete)
    ticket_interprete_3.date_heure_ticket = (
        ticket_interprete_1.date_heure_ticket + timedelta(days=4)
    )  # 4 jours après

    client_id = 30

    insere_ticket(ticket_interprete_1, client_id)
    insere_ticket(ticket_interprete_2, client_id)
    insere_ticket(ticket_interprete_3, client_id)

    tickets = TicketService.get_tickets(
        session, client_id=client_id, date_fin=ticket_interprete_2.date_heure_ticket
    )
    assert len(tickets) == 2
    assert compare_ignorant_ticket_ligne_id(
        tickets[0],
        TicketEnteteResponse(
            ticket_id=tickets[0].ticket_id,
            client_id=client_id,
            date_heure_ticket=ticket_interprete_1.date_heure_ticket,
            enseigne_id=1,
            montant_total_ticket=35.55,
            lignes=[
                TicketLigneResponse(
                    ticket_ligne_id=1,  # ignoré
                    libelle_produit="*100G NENTOS FESH H",
                    quantite=4,
                    categorie_produit_id=1,
                    nom_categorie_produit="Fruits & légumes",
                    prix_unitaire=3.54,
                    montant_total_ligne=14.16,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=2,  # ignoré
                    libelle_produit="*606G SORB CIT MX",
                    quantite=1,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=None,
                    montant_total_ligne=2.29,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=3,  # ignoré
                    libelle_produit="*650G BAC POMME CHF",
                    quantite=2,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=9.55,
                    montant_total_ligne=19.1,
                ),
            ],
        ),
    )
    assert compare_ignorant_ticket_ligne_id(
        tickets[1],
        TicketEnteteResponse(
            ticket_id=tickets[1].ticket_id,
            client_id=client_id,
            date_heure_ticket=ticket_interprete_2.date_heure_ticket,
            enseigne_id=1,
            montant_total_ticket=35.55,
            lignes=[
                TicketLigneResponse(
                    ticket_ligne_id=1,  # ignoré
                    libelle_produit="*100G NENTOS FESH H",
                    quantite=4,
                    categorie_produit_id=1,
                    nom_categorie_produit="Fruits & légumes",
                    prix_unitaire=3.54,
                    montant_total_ligne=14.16,
                ),
                TicketLigneResponse(
                    ticket_ligne_id=2,  # ignoré
                    libelle_produit="*606G SORB CIT MX",
                    quantite=1,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=None,
                    montant_total_ligne=2.29,
                ),
                TicketLigneResponse(  # ignoré
                    ticket_ligne_id=3,
                    libelle_produit="*650G BAC POMME CHF",
                    quantite=2,
                    categorie_produit_id=2,
                    nom_categorie_produit="Viandes & poissons",
                    prix_unitaire=9.55,
                    montant_total_ligne=19.1,
                ),
            ],
        ),
    )
