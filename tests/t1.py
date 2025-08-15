# tests/t1.py
from sqlmodel import Session
from api.database import engine  # Import direct depuis ton fichier
from api.services.client_service import ClientService

def test_get_all_clients():
    # Crée une session manuellement avec ton engine existant
    with Session(engine) as session:
        clients = ClientService.get_all_clients(session)
        print(clients)  # Affiche la liste des clients

if __name__ == "__main__":
    test_get_all_clients()