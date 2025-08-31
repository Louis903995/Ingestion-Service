from fastapi import APIRouter
from app.schemas.allures import AlluresResponse
from app.services.allures_service import generate_allures

router = APIRouter()

@router.get("/clients/{client_id}/allures/", response_model=AlluresResponse)
async def get_allures():
    return generate_allures()

