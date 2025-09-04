from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.ticket import TicketEntete
from app.schemas.allures import AlluresResponse, MesureTemporelle

class AlllureService:
    @staticmethod
    def get_allures(session: Session, client_id: int, n_semaines: int) -> AlluresResponse:
        depense_constate = []
        depense_predite = [
            MesureTemporelle(d=datetime(2025, 9, 8, 0, 0), v=120)
        ]

        # Pas besoin de 'with' ou 'next', la session est déjà ouverte
        statement = (
            select(TicketEntete)
            .where(TicketEntete.client_id == client_id)
            .order_by(TicketEntete.date_heure_ticket)
        )
        tickets = session.exec(statement).all()

        if not tickets:
            return AlluresResponse(
                depense_constate=depense_constate, depense_predite=depense_predite
            )

        def get_monday(d: datetime) -> datetime:
            return (
                d
                - timedelta(
                    days=d.weekday(),
                    hours=d.hour,
                    minutes=d.minute,
                    seconds=d.second,
                    microseconds=d.microsecond,
                )
                + timedelta(seconds=1)
            )

        current_monday = get_monday(tickets[0].date_heure_ticket)
        week_total = 0.0

        for ticket in tickets:
            if ticket.date_heure_ticket >= current_monday + timedelta(days=7):
                depense_constate.append(MesureTemporelle(d=current_monday, v=week_total))
                current_monday = get_monday(ticket.date_heure_ticket)
                week_total = 0.0
            week_total += ticket.montant_total_ticket or 0.0

        depense_constate.append(MesureTemporelle(d=current_monday, v=week_total))
        depense_constate = depense_constate[-n_semaines:]

        return AlluresResponse(
            depense_constate=depense_constate, depense_predite=depense_predite
        )
