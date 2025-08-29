from fastapi import APIRouter
from app.schemas.times import DataResponse
from app.services.times import get_valeurs


data_router = APIRouter(prefix="/data", tags=["Data"])

@data_router.get("/", response_model=DataResponse)
def get_data():
    valeurs_passees, valeur_actuelle = get_valeurs()
    return DataResponse(valeurs_passees=valeurs_passees, valeur_actuelle=valeur_actuelle)
