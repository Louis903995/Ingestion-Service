from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional

from app.services.ticket_service import TicketService
from app.db.database import get_session
from app.schemas.ticket_interprete import TicketInterprete
from app.schemas.ticket_reponse import TicketEnteteResponse

router = APIRouter()


@router.post("/clients/{client_id}/tickets", response_model=TicketEnteteResponse)
def create_ticket(
    client_id: int,
    ticket_scanne: TicketInterprete,
    session: Session = Depends(get_session),
):
    ticket = TicketService.create_ticket(session, client_id, ticket_scanne)
    if not ticket:
        raise HTTPException(
            status_code=400, detail="Erreur lors de la création du ticket"
        )
    return ticket


@router.get("/clients/{client_id}/tickets", response_model=List[TicketEnteteResponse])
def get_tickets(
    client_id: int,
    date_debut: Optional[str] = Query(None),
    date_fin: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    return TicketService.get_tickets(session, client_id, date_debut, date_fin)


@router.get("/clients/{client_id}/depenses", response_model=float)
def get_depenses_par_categorie(
    client_id: int,
    date_debut: Optional[str] = Query(None),
    date_fin: Optional[str] = Query(None),
    categorie_id: Optional[int] = Query(None),
    session: Session = Depends(get_session),
):
    return TicketService.get_montant_total_par_categorie(
        session, client_id, date_debut, date_fin, categorie_id
    )
