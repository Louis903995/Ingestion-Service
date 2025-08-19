import logging
import os
from mistralai import Mistral
import requests
import app.db.database
from app.metrics import COMPTEUR_INGESTIONS_TICKET_ERREUR
from app.schemas.ticket_interprete import TicketInterprete
from app.services.enseigne_service import EnseigneService
from app.services.tickets.reconnaissance_tickets.resolver import extrait_ticket_scanne


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def interprete_image(base64_image: bytes) -> TicketInterprete | None:
    try:
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
    except Exception as e:
        logger.error(e)


# retrouve l'id de l'enseigne en fonction du nom d'enseigne scanné
# et ajoute la propriété "id_enseigne" ainsi que la valeur de l'id
def resoud_enseigne(ticket: TicketInterprete) -> TicketInterprete | None:
    enseigne_id = EnseigneService.trouve_enseigne_id(
        app.db.database.enseignes_dict, ticket.nom_enseigne, ticket.tel_enseigne
    )
    if enseigne_id:
        ticket.enseigne_id = enseigne_id
        return ticket
    else:
        logger.warning("Impossible de trouver une correspondance d'enseigne")


# itere sur toutes les lignes du ticket et
# ajoute la propriété "categorie_produit_id" lorsque elle est trouvée
def categorise_produits(ticket: TicketInterprete) -> TicketInterprete | None:
    try:

        def resoud_categorie_id(produit_categorie):
            for k in app.db.database.produit_categorie_dict:
                if k.lower() == produit_categorie.lower():
                    return app.db.database.produit_categorie_dict.get(k)
            return app.db.database.produit_categorie_dict["Aucune"]

        payload = {"produits": [ligne.libelle_produit for ligne in ticket.lignes]}
        response = requests.post(
            f"{os.environ.get('CATEGORISATION_SERVICE_URL')}/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            predictions = response.json()["predictions"]
            pred_dico = {item["produit"]: item["categorie"] for item in predictions}
            for ligne in ticket.lignes:
                produit_categorie = pred_dico[ligne.libelle_produit]
                categorie_produit_id = resoud_categorie_id(produit_categorie)
                ligne.categorie_produit_id = categorie_produit_id
        return ticket
    except Exception as e:
        logger.error(e)


# analyse une image de ticket et le stocke dans les différentes tables en l'attachant au user id
# renvoie l'id du ticket, None en cas d'erreur
def ingere_image(client_id: int, base64_image: bytes) -> TicketInterprete | None:
    ticket_brut = interprete_image(base64_image)
    if not ticket_brut:
        COMPTEUR_INGESTIONS_TICKET_ERREUR.add(1, {"cause": "OCR impossible"})
    else:
        ticket_enrichi_intermediaire = categorise_produits(ticket_brut)
        if not ticket_enrichi_intermediaire:
            COMPTEUR_INGESTIONS_TICKET_ERREUR.add(
                1, {"cause": "Categorisation produit impossible"}
            )
        else:
            ticket_enrichi = resoud_enseigne(ticket_enrichi_intermediaire)
            if not ticket_enrichi:
                COMPTEUR_INGESTIONS_TICKET_ERREUR.add(
                    1, {"cause": "Resolution enseigne impossible"}
                )
            else:
                return ticket_enrichi
    return None  # pas utile mais joli
