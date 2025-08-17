import re

from app.schemas.ticket_interprete import TicketInterprete
from reconnaissance_tickets.enseignes.carrefour.commun import (
    interprete_lignes,
    isole_lignes_tableau,
    trouve_date_heure,
    trouve_tel_enseigne,
)



def trouve_nom_enseigne_crf_city(texte: str) -> str | None:
    # Recherche "#" suivi de 0 ou plusieurs espaces puis "city", insensible à la casse.
    # recherche toute ligne non vide après "city"
    # capture le début de la ligne jusqu'à "Tel" non inclus
    match = re.search(
        r"#\s*city[\s\n]*(.*?)(?=\s*Tel:)", texte, re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()


def extrait_ticket_scanne(markdown: str) -> TicketInterprete:
    return TicketInterprete(
        nom_enseigne=trouve_nom_enseigne_crf_city(markdown),
        tel_enseigne=trouve_tel_enseigne(markdown),
        date_heure_ticket=trouve_date_heure(markdown),
        montant_total_ticket=0.0,
        lignes=interprete_lignes(isole_lignes_tableau(markdown)),
    )
