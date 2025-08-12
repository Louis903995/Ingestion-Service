from sqlmodel import Session, select
from fastapi import HTTPException
from models.ticket import Ticket

class TicketService:
    
    @staticmethod
    def get_all_tickets(session: Session):
        return session.exec(select(Ticket)).all()
    
    @staticmethod
    def get_ticket_by_id(session: Session, ticket_id: int):
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket non trouvé")
        return ticket
    
    @staticmethod
    def create_ticket(session: Session, ticket: Ticket):
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket
    
    @staticmethod
    def update_ticket(session: Session, ticket_id: int, ticket_update: Ticket):
        db_ticket = session.get(Ticket, ticket_id)
        if not db_ticket:
            raise HTTPException(status_code=404, detail="Ticket non trouvé")

        for key, value in ticket_update.dict(exclude_unset=True).items():
            setattr(db_ticket, key, value)

        session.add(db_ticket)
        session.commit()
        session.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def delete_ticket(session: Session, ticket_id: int):
        db_ticket = session.get(Ticket, ticket_id)
        if not db_ticket:
            raise HTTPException(status_code=404, detail="Ticket non trouvé")

        session.delete(db_ticket)
        session.commit()
        return {"message": "Ticket supprimé avec succès"}