import os
from datetime import datetime, timedelta
import requests
from sqlmodel import Session, select
from app.models.ticket import TicketEntete
from app.schemas.allures import AlluresResponse, MesureTemporelle


# renvoie le ludi qui précède immediatement la datetime d
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


class AlllureService:
    @staticmethod
    def get_allures(
        session: Session, client_id: int, n_semaines: int
    ) -> AlluresResponse:
        depense_constate = []
        statement = (
            select(TicketEntete)
            .where(TicketEntete.client_id == client_id)
            .order_by(TicketEntete.date_heure_ticket)
        )
        tickets = session.exec(statement).all()
        if not tickets:
            return AlluresResponse(depense_constate=[], depense_predite=[])

        current_monday = get_monday(tickets[0].date_heure_ticket)
        week_total = 0.0
        for ticket in tickets:
            if ticket.date_heure_ticket >= current_monday + timedelta(days=7):
                depense_constate.append(
                    MesureTemporelle(d=current_monday, v=week_total)
                )
                current_monday = get_monday(ticket.date_heure_ticket)
                week_total = 0.0
            week_total += ticket.montant_total_ticket or 0.0
        depense_constate.append(MesureTemporelle(d=current_monday, v=week_total))
        depense_constate = depense_constate[-n_semaines:]

        url = os.environ.get("TIMESERIES_SERVICE_URL")
        if not url:
            raise ValueError("TIMESERIES_SERVICE_URL non défini")

        # Conversion de depense_constate en liste de dictionnaires avec datetime en ISO format
        depense_constate_dicts = []
        for mesure in depense_constate:
            mesure_dict = mesure.model_dump()
            mesure_dict["d"] = mesure.d.isoformat()  # Convertit datetime en chaîne ISO
            depense_constate_dicts.append(mesure_dict)

        try:
            response = requests.post(
                f"{url}/predictions/",
                json=depense_constate_dicts,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                # Conversion de la réponse en liste de MesureTemporelle
                depense_predite = []
                for item in response.json():
                    # Convertit la chaîne ISO en datetime
                    item["d"] = datetime.fromisoformat(item["d"])
                    depense_predite.append(MesureTemporelle(**item))
            else:
                depense_predite = []

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'appel au service de prédiction : {e}")
            depense_predite = []

        return AlluresResponse(
            depense_constate=depense_constate, depense_predite=depense_predite
        )
