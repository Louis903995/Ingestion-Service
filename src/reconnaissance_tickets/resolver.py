import re
from reconnaissance_tickets.model_ticket import TicketScanne
from reconnaissance_tickets.enseignes.carrefour.carrefour_city import (
    extrait_ticket_scanne as crf_city_extrait_ticket_scanne,
)
from reconnaissance_tickets.enseignes.carrefour.carrefour_market import (
    extrait_ticket_scanne as crf_mkt_extrait_ticket_scanne,
)


def extrait_ticket_scanne(markdown: str) -> TicketScanne | None:
    if re.search(r"^[\s\n]*#\s*city", markdown, re.IGNORECASE | re.MULTILINE):
        return crf_city_extrait_ticket_scanne(markdown)
    if re.search(r"^[\s\n]*#\s*market", markdown, re.IGNORECASE | re.MULTILINE):
        return crf_mkt_extrait_ticket_scanne(markdown)
    return None


# with open("sample.md", "r") as f:
#     print(extrait_ticket_scanne(f.read()).model_dump_json())
# print("-------------------------")
# with open("sample-modifié.md", "r") as f:
#     print(extrait_ticket_scanne(f.read()).model_dump_json())
# print("-------------------------")
# with open("sample-crf-city.md", "r") as f:
#     print(extrait_ticket_scanne(f.read()).model_dump_json())
# print("-------------------------")
