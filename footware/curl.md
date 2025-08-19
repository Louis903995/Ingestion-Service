curl -X POST "http://localhost:8000/clients/123/tickets_tmp" \
-H "Content-Type: application/json" \
-d '{
    "nom_enseigne": "Supermarché X",
    "enseigne_id": 1,
    "tel_enseigne": "0123456789",
    "date_heure_ticket": "2025-08-18T12:00:00",
    "montant_total_ticket": 50.99,
    "lignes": [
        {
            "taux_tva": 6,
            "libelle_produit": "Produit A",
            "qte": 2,
            "categorie_produit_id": 1,
            "pu": 10.50,
            "montant": 21.00
        },
        {
            "taux_tva": 5,
            "libelle_produit": "Produit B",
            "qte": 1,
            "categorie_produit_id": 3,
            "pu": 25.99,
            "montant": 25.99
        }
    ]
}'


curl -X POST "http://localhost:8000/clients/123/tickets" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@tests/reconnaissance_tickets/data/source/carrefour_city_1.jpg"

  curl -X POST "https://ingestion-service.politesky-11b41c05.westeurope.azurecontainerapps.io/clients/123/tickets" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@tests/reconnaissance_tickets/data/source/carrefour_city_1.jpg"