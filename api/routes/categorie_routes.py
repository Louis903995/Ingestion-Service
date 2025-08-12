from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from Model.categorie import Categorie
from Service.categorie_service import CategorieService
from database import get_session

router = APIRouter()

@router.get("/categories", response_model=List[Categorie])
def read_categories(session: Session = Depends(get_session)):
    return CategorieService.get_all_categories(session)

@router.get("/categories/{categorie_id}", response_model=Categorie)
def read_category(categorie_id: int, session: Session = Depends(get_session)):
    return CategorieService.get_category_by_id(session, categorie_id)

@router.post("/categories", response_model=Categorie)
def create_category(category: Categorie, session: Session = Depends(get_session)):
    return CategorieService.create_category(session, category)

@router.put("/categories/{categorie_id}", response_model=Categorie)
def update_category(categorie_id: int, category_update: Categorie, session: Session = Depends(get_session)):
    return CategorieService.update_category(session, categorie_id, category_update)

@router.delete("/categories/{categorie_id}")
def delete_category(categorie_id: int, session: Session = Depends(get_session)):
    return CategorieService.delete_category(session, categorie_id)