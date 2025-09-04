from fastapi import APIRouter, Depends
from app.schemas.allures import AlluresResponse
from app.services.allures_service import AlllureService
from sqlmodel import Session
from app.db.database import get_session


router = APIRouter()


@router.get("/clients/{client_id}/allures", response_model=AlluresResponse)
async def get_allures(client_id: int, session: Session = Depends(get_session)):
    return AlllureService.get_allures(session, client_id, 4)
