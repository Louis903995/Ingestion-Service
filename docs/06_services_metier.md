# 06 — Services métiers

Aperçu:
- TicketService (app/services/ticket_service.py): persistence, requêtes et agrégations.
- ingestion_ticket (app/services/tickets/ingestion_ticket.py): OCR, catégorisation, résolution enseigne.
- EnseigneService (app/services/enseigne_service.py): accès enseignes + matching flou.
- ProduitCategorieService (app/services/produit_categorie_service.py): accès catégories + dictionnaire mémoire.
- ClientService (app/services/client_service.py): CRUD clients.

Diagramme de classes (services → modèles/schémas):

```mermaid
classDiagram
  class TicketService {
    +create_ticket(session, client_id, ticket_scanne)
    +get_tickets(session, client_id, date_debut?, date_fin?)
    +get_montant_total_par_categorie(session, client_id, date_debut?, date_fin?, categorie_id?)
    +ingere_image(session, client_id, base64_image)
  }
  class EnseigneService {
    +get_all_enseignes(session)
    +get_enseigne_by_id(session, id)
    +get_enseignes_dict(session)
    +trouve_enseigne_id(enseignes, nom, tel?, seuil, poids_nom, poids_tel)
  }
  class ProduitCategorieService {
    +get_all_produit_categories(session)
    +get_produit_categorie_by_id(session, id)
    +get_produit_categorie_dict(session)
  }
  class ClientService {
    +get_all_clients(session)
    +get_client_by_id(session, id)
    +create_client(session, payload)
    +update_client(session, id, payload)
    +delete_client(session, id)
  }
  TicketService --> TicketEntete
  TicketService --> TicketLignes
  TicketService --> TicketInterprete
  ProduitCategorieService --> ProduitCategorie
  EnseigneService --> Enseigne
  ClientService --> Client
```

Détails clés:
- TicketService.create_ticket:
  - Transforme TicketInterprete (DTO) en TicketEntete/TicketLignes (SQLModel).
  - Utilise model_validate pour garantir la cohérence.
- TicketService.get_tickets:
  - Récupère les lignes par ticket, joint la catégorie (selectinload) et renvoie des DTO de réponse.
- TicketService.get_montant_total_par_categorie:
  - Calcule un SUM sur les lignes filtrées par période et catégorie.
- ingestion_ticket.ingere_image:
  - Enchaîne OCR → catégorisation → résolution enseigne. Incrémente les métriques d’erreurs si besoin.

Navigation:
- API: [07 — API et routes](./07_api_endpoints.md)
- DB/Config/Metrics: [08 — Base & métriques](./08_bdd_config_metrics.md)
- Points d’attention: [10 — Points d’attention](./10_points_attention.md)

Voir aussi: [Sommaire](./00_navigation.md)