from sqlmodel import Session
from api.database import engine
from api.services.client_service import ClientService
from api.services.enseigne_service import EnseigneService
from api.services.ticket_service import TicketService


def test_get_all_clients():
    with Session(engine) as session:
        clients = ClientService.get_all_clients(session)
        print(clients)


def test_get_all_enseignes():
    with Session(engine) as session:
        # enseignes = EnseigneService.get_all_enseignes(session)
        enseignes = EnseigneService.get_enseignes_dict(session)
        print(EnseigneService.trouve_enseigne_id(enseignes, "Marke1 Basievx"))
        # print(enseignes)


def test_get_all_tickets():
    with Session(engine) as session:
        tickets = TicketService.get_ticket_with_lignes_and_categorie_nom(session, 1)
        print(tickets)


if __name__ == "__main__":
    test_get_all_tickets()
