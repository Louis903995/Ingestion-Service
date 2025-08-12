from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from Model.ticket import Ticket
from Service.ticket_service import TicketService
from database import get_session

router = APIRouter()

@router.get("/tickets", response_model=List[Ticket])
def read_tickets(session: Session = Depends(get_session)):
    return TicketService.get_all_tickets(session)

@router.get("/tickets/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: int, session: Session = Depends(get_session)):
    return TicketService.get_ticket_by_id(session, ticket_id)

@router.post("/tickets", response_model=Ticket)
def create_ticket(ticket: Ticket, session: Session = Depends(get_session)):
    return TicketService.create_ticket(session, ticket)

@router.put("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket_update: Ticket, session: Session = Depends(get_session)):
    return TicketService.update_ticket(session, ticket_id, ticket_update)

@router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, session: Session = Depends(get_session)):
    return TicketService.delete_ticket(session, ticket_id)