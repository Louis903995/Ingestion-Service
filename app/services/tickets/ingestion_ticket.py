from app.api.database import engine
from sqlmodel import Session
from app.schemas.ticket_interprete import TicketInterprete

import os
from mistralai import Mistral

from app.services.enseigne_service import EnseigneService
from app.services.tickets.reconnaissance_tickets.resolver import extrait_ticket_scanne

enseignes_dict = None
with Session(engine) as session:
    enseignes_dict = EnseigneService.get_enseignes_dict(session)


def interprete_image(base64_image: bytes) -> TicketInterprete | None:
    MISTRAL_KEY = os.environ.get("MISTRAL_API_KEY")
    if MISTRAL_KEY:
        client = Mistral(api_key=MISTRAL_KEY)
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}",
            },
            include_image_base64=True,
        )
        return extrait_ticket_scanne(ocr_response.pages[0].markdown)


# retrouve l'id de l'enseigne en fonction du nom d'enseigne scanné
# et ajoute la propriété "id_enseigne" ainsi que la valeur de l'id
def resoud_enseigne(ticket: TicketInterprete) -> dict:
    x = EnseigneService.trouve_enseigne_id(
        enseignes_dict, ticket.nom_enseigne, ticket.tel_enseigne
    )
    print(x)
    return ticket


# itere sur toutes les lignes du ticket et
# ajoute la propriété "categorie_produit_id" lorsque elle est trouvée
def categorise_produits(ticket: TicketInterprete) -> dict:
    return ticket


# ajoute le nouvel entete dans la table "ticket_entete"
# renvoie l'identifiant du ticket, None en cas d'erreur
def write_ticket_entete(user_id, ticket: TicketInterprete) -> int | None:
    return 1


# analyse une image de ticket et le stocke dans les différentes tables en l'attachant au user id
# renvoie l'id du ticket, None en cas d'erreur
def ingere_image(user_id: int, base64_image: bytes) -> int | None:
    ticket_brut = interprete_image(base64_image)
    ticket_categorise = categorise_produits(ticket_brut)
    ticket_avec_enseigne = resoud_enseigne(ticket_categorise)
    return write_ticket_entete(user_id, ticket_avec_enseigne)
