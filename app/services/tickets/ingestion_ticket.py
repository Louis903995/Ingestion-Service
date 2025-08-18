import os
from mistralai import Mistral
import requests
import app.db.database
from app.schemas.ticket_interprete import TicketInterprete
from app.services.enseigne_service import EnseigneService
from app.services.tickets.reconnaissance_tickets.resolver import extrait_ticket_scanne


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
def resoud_enseigne(ticket: TicketInterprete) -> TicketInterprete:
    enseigne_id = EnseigneService.trouve_enseigne_id(
        app.db.database.enseignes_dict, ticket.nom_enseigne, ticket.tel_enseigne
    )
    if enseigne_id:
        ticket.enseigne_id = enseigne_id
    else:
        pass  # on va monitorer
    return ticket


# itere sur toutes les lignes du ticket et
# ajoute la propriété "categorie_produit_id" lorsque elle est trouvée
def categorise_produits(ticket: TicketInterprete) -> TicketInterprete:
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


# analyse une image de ticket et le stocke dans les différentes tables en l'attachant au user id
# renvoie l'id du ticket, None en cas d'erreur
def ingere_image(client_id: int, base64_image: bytes) -> TicketInterprete | None:
    ticket_brut = interprete_image(base64_image)
    ticket_enrichi_intermediaire = categorise_produits(ticket_brut)
    ticket_enrichi = resoud_enseigne(ticket_enrichi_intermediaire)
    return ticket_enrichi
