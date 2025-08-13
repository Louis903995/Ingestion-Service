from datetime import datetime


# transforme l'image en un json (dict) intermédiaire
def ocr_to_dict(image: bytes) -> dict:
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
                " montant_total_ligne": 12.1,
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
def write_ticket_entete(user_id, ticket: dict) -> int | None:
    return 1


# ajoute chacune des lignes de tickets dans la table "ticket_ligne"
# renvoie le nombre de lignes écrites, None en cas d'erreur
def write_ticket_ligne(ticket_id: int, ticket: dict) -> int | None:
    return 2


# analyse une image de ticket et le stocke dans les différentes tables en l'attachant au user id
# renvoie l'id du ticket, None en cas d'erreur
def ingestion_image(user_id: int, image: bytes) -> int | None:
    ticket_dict = ocr_to_dict(image)
    ticket_categorise = categorise_produits(ticket_dict)
    ticket_lu = resoud_enseigne(ticket_categorise)
    ticket_id = write_ticket_entete(user_id, ticket_lu)
    if ticket_id:
        lignes_ecrites = write_ticket_ligne(ticket_id, ticket_lu)
        if lignes_ecrites == len(ticket_lu["lignes"]):
            return ticket_id
    return None
