from datetime import datetime
from load_env import load_env_file_to_environ
import os
from mistralai import Mistral

from reconnaissance_tickets.model_ticket import LigneTicketScanne, TicketScanne
from reconnaissance_tickets.resolver import extrait_ticket_scanne


load_env_file_to_environ()


# transforme l'image en TicketScanne
def ocr_to_dict(base64_image: bytes) -> TicketScanne | None:
    MISTRAL_KEY = os.environ.get("MISTRAL-API-KEY")
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
        # print(ocr_response)
        # with open("sample-crf-city.md", "w", encoding="utf-8") as f:
        #     f.write(ocr_response.pages[0].markdown)
    else:
        # traiter le cas où ne trouve pas dans os.environ
        pass
    return {
        "entete": {
            "nom_enseigne": "Carrefour Market Loos",
            "date_heure_ticket": datetime(2025, 8, 10, 10, 00, 00),
            "montant_total_ticket": 45.8,
        },
        "lignes": [
            {
                "libelle_produit": "Coca cola",
                "quantite": 1,
                "prix_unitaire": 12,
                "montant_total_ligne": 12.1,
            },
            {
                "libelle_produit": "Perrier 50 cl",
                "quantite": 2,
                "prix_unitaire": 2,
                "montant_total_ligne": 4,
            },
            # etc....
        ],
    }


# retrouve l'id de l'enseigne en fonction du nom d'enseigne scanné
# et ajoute la propriété "id_enseigne" ainsi que la valeur de l'id
def resoud_enseigne(ticket: dict) -> dict:
    return ticket


# itere sur toutes les lignes du ticket et
# ajoute la propriété "categorie_produit_id" lorsque elle est trouvée
def categorise_produits(ticket: dict) -> dict:
    return ticket


# ajoute le nouvel entete dans la table "ticket_entete"
# renvoie l'identifiant du ticket, None en cas d'erreur
def write_ticket_entete(user_id, ticket: TicketScanne) -> int | None:
    return 1


# ajoute chacune des lignes de tickets dans la table "ticket_ligne"
# renvoie le nombre de lignes écrites, None en cas d'erreur
def write_ticket_ligne(ticket_id: int, ticket: LigneTicketScanne) -> int | None:
    return 2


# analyse une image de ticket et le stocke dans les différentes tables en l'attachant au user id
# renvoie l'id du ticket, None en cas d'erreur
def ingestion_image(user_id: int, base64_image: bytes) -> int | None:
    ticket_brut = ocr_to_dict(base64_image)
    # ticket_categorise = categorise_produits(ticket_brut)
    # ticket_avec_enseigne = resoud_enseigne(ticket_categorise)
    # ticket_id = write_ticket_entete(user_id, ticket_avec_enseigne)
    print (ticket_brut)
    # if ticket_id:
    #     # lignes_ecrites = write_ticket_ligne(ticket_id, ticket_avec_enseigne)
    #     # if lignes_ecrites == len(ticket_avec_enseigne["lignes"]):
    #     return ticket_id
    return None
