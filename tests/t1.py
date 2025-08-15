from sqlmodel import Session
from api.database import engine
from api.services.client_service import ClientService
from api.services.enseigne_service import EnseigneService


def test_get_all_clients():
    with Session(engine) as session:
        clients = ClientService.get_all_clients(session)
        print(clients)


def test_get_all_enseignes():
    with Session(engine) as session:
        # enseignes = EnseigneService.get_all_enseignes(session)
        enseignes = EnseigneService.get_enseignes_dict(session)
        print (EnseigneService.trouve_enseigne_id(enseignes, "Marke1 Basievx"))
        # print(enseignes)


if __name__ == "__main__":
    test_get_all_enseignes()
