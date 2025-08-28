from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException
from app.schemas.client import ClientResponse
from app.models.client import Client


class ClientService:

    @staticmethod
    def get_all_clients(session: Session) -> List[ClientResponse]:
        return session.exec(select(Client)).all()

    @staticmethod
    def get_client_by_id(session: Session, client_id: int) -> ClientResponse:
        client = session.get(Client, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        return client

    # @staticmethod
    # def create_client(session: Session, client_create: ClientCreate):
    #     client = Client.from_orm(client_create)
    #     session.add(client)
    #     session.commit()
    #     session.refresh(client)
    #     return client

    # @staticmethod
    # def update_client(session: Session, client_id: int, client_update: ClientUpdate):
    #     db_client = session.get(Client, client_id)
    #     if not db_client:
    #         raise HTTPException(status_code=404, detail="Client non trouvé")

    #     update_data = client_update.dict(exclude_unset=True)
    #     if not update_data:
    #         raise HTTPException(status_code=400, detail="Aucune donnée à mettre à jour")

    #     for key, value in update_data.items():
    #         setattr(db_client, key, value)

    #     db_client.date_derniere_modification = datetime.datetime.utcnow()

    #     session.add(db_client)
    #     session.commit()
    #     session.refresh(db_client)
    #     return db_client

    # @staticmethod
    # def delete_client(session: Session, client_id: int):
    #     client = session.get(Client, client_id)
    #     if not client:
    #         raise HTTPException(status_code=404, detail="Client non trouvé")

    #     session.delete(client)
    #     session.commit()
    #     return {"message": "Client supprimé avec succès"}
