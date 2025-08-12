from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from Model.supermarche import Supermarche
from Service.supermarche_service import SupermarcheService
from database import get_session

router = APIRouter()

@router.get("/supermarches", response_model=List[Supermarche])
def read_supermarches(session: Session = Depends(get_session)):
    return SupermarcheService.get_all_supermarches(session)

@router.get("/supermarches/{supermarche_id}", response_model=Supermarche)
def read_supermarche(supermarche_id: int, session: Session = Depends(get_session)):
    return SupermarcheService.get_supermarche_by_id(session, supermarche_id)

@router.post("/supermarches", response_model=Supermarche)
def create_supermarche(supermarche: Supermarche, session: Session = Depends(get_session)):
    return SupermarcheService.create_supermarche(session, supermarche)

@router.put("/supermarches/{supermarche_id}", response_model=Supermarche)
def update_supermarche(supermarche_id: int, supermarche_update: Supermarche, session: Session = Depends(get_session)):
    return SupermarcheService.update_supermarche(session, supermarche_id, supermarche_update)

@router.delete("/supermarches/{supermarche_id}")
def delete_supermarche(supermarche_id: int, session: Session = Depends(get_session)):
    return SupermarcheService.delete_supermarche(session, supermarche_id)