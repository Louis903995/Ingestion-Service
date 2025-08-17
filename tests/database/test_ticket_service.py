import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from datetime import datetime, timedelta
from tests.database.fixtures import (
    session,
    nettoie_tout,
    PYODBC_CONNECTION_STRING,
    DB_NAME_TEST,
)


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


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    execute_script_sql(
        "sql/ajoute_categories.sql", DB_NAME_TEST, PYODBC_CONNECTION_STRING
    )
    yield


# @pytest.fixture(scope="module", autouse=True)
# def teardown_module():
#     """Exécuté UNE SEULE FOIS après tous les tests du module."""
#     yield  # Le code après yield s'exécute après tous les tests
#     print("\n🌳 [TEARDOWN MODULE] Nettoyage global (ex: supprimer la base de données)")


# # Méthode exécutée AVANT chaque test
# @pytest.fixture(autouse=True, scope="function")
# def setup():
#     print("\n⏳ [SETUP] Avant le test")
#     # Code d'initialisation (ex: créer une base de données, préparer des données)
#     yield


# # Méthode exécutée APRES chaque test
# @pytest.fixture(autouse=True, scope="function")
# def teardown():
#     yield  # Le test s'exécute ici
#     print("\n🧹 [TEARDOWN] Après le test")
#     # Code de nettoyage (ex: supprimer des fichiers, vider une base)


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
                "montant": 4.35,
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
                "montant": 2.49,
                "categorie_produit_id": 1
            }
        ]
}"""
    )

    # return TicketInterprete(
    #     nom_enseigne="Leclerc",
    #     tel_enseigne="0102030405",
    #     date_heure_ticket=datetime(2025, 8, 16, 9, 0),
    #     montant_total_ticket=12.5,
    #     lignes=[
    #         LigneTicketInterpretee(
    #             taux_tva=5, libelle_produit="Pain", qte=2, pu=1.0, montant=2.0
    #         ),
    #         LigneTicketInterpretee(
    #             taux_tva=20, libelle_produit="Vin", qte=1, pu=10.5, montant=10.5
    #         ),
    #     ],
    # )


def test_create_ticket(session, simple_ticket_scanne):
    user_id = 42
    ticket = TicketService.create_ticket(session, user_id, simple_ticket_scanne)
    print(ticket)
    # assert ticket.ticket_id is not None
    # assert ticket.client_id == user_id
    # assert ticket.montant_total_ticket == 12.5

    # lignes = session.exec(
    #     select(TicketLignes).where(TicketLignes.ticket_id == ticket.ticket_id)
    # ).all()
    # assert len(lignes) == 2
    # assert lignes[0].libelle_produit == "Pain"
    # assert lignes[1].libelle_produit == "Vin"


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
#     dt_min = datetime(2025, 8, 15)
#     dt_max = datetime(2025, 8, 17)
#     tickets2 = TicketService.get_tickets(
#         session, client_id=user_id, date_debut=dt_min, date_fin=dt_max
#     )
#     assert len(tickets2) == 1

#     dt_trop_tot = datetime(2025, 8, 10)
#     dt_trop_tard = datetime(2025, 8, 12)
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
