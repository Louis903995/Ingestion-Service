import re

from app.schemas.ticket_interprete import TicketInterprete
from app.services.tickets.reconnaissance_tickets.enseignes.carrefour.carrefour_city import (
    extrait_ticket_scanne as crf_city_extrait_ticket_scanne,
)
from app.services.tickets.reconnaissance_tickets.enseignes.carrefour.carrefour_market import (
    extrait_ticket_scanne as crf_mkt_extrait_ticket_scanne,
)


def extrait_ticket_scanne(markdown: str) -> TicketInterprete | None:
    if re.search(r"^[\s\n]*#\s*city", markdown, re.IGNORECASE | re.MULTILINE):
        return crf_city_extrait_ticket_scanne(markdown)
    if re.search(r"^[\s\n]*#\s*market", markdown, re.IGNORECASE | re.MULTILINE):
        return crf_mkt_extrait_ticket_scanne(markdown)
    return None
