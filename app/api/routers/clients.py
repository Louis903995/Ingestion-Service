from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from ..models.client import Client
from ..schemas.client import ClientCreate, ClientUpdate
from ..services.client_service import ClientService
from ..database import get_session

router = APIRouter()

@router.get("/clients", response_model=List[Client])
def read_clients(session: Session = Depends(get_session)):
    return ClientService.get_all_clients(session)

@router.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, session: Session = Depends(get_session)):
    return ClientService.get_client_by_id(session, client_id)

@router.post("/clients", response_model=Client)
def create_client(client_create: ClientCreate, session: Session = Depends(get_session)):
    return ClientService.create_client(session, client_create)

@router.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client_update: ClientUpdate, session: Session = Depends(get_session)):
    return ClientService.update_client(session, client_id, client_update)

@router.delete("/clients/{client_id}")
def delete_client(client_id: int, session: Session = Depends(get_session)):
    return ClientService.delete_client(session, client_id)