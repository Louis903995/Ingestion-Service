# 10 — Points d’attention, divergences et améliorations

Cette section recense des éléments relevés dans les fichiers fournis qui méritent une attention particulière.

Incohérences/bugs potentiels:
1) Types de dates dans ticket_service et router
- Router (ticket.get_tickets) passe date_debut et date_fin en Optional[str].
- Service (TicketService.get_tickets) attend Optional[datetime].
- Action: parser les dates dans le router (ou accepter str et parser dans le service).

2) Conversion vers TicketEnteteResponse
- Le service utilise ticket.date_heure_ticket.isoformat() alors que le schéma de réponse tape datetime. Pydantic peut parser, mais mieux vaut renvoyer directement un datetime pour cohérence.

3) Création/mise à jour Client (ClientService)
- ClientCreate/ClientUpdate utilisent des champs nom, prenom, … alors que le modèle Client définit nom_client, prenom_client, …
- Client.from_orm(client_create) ne correspondra pas (mappage de noms). Les updates via setattr(db_client, key, value) échoueront ou créeront des attributs non persistés.
- Action: aligner les noms de champs ou introduire un mapping explicite.

4) Import de get_session dans routers/clients.py
- from ..database import get_session semble incorrect (la fonction est dans app/db/database.py).
- Action: corriger en from app.db.database import get_session (ou via un __init__ correctement exposé).

5) Annotations de type
- ProduitCategorieService.get_produit_categorie_dict: dict[str:int] n’est pas une annotation valide; utiliser dict[str, int] ou Dict[str, int].
- ingestion_ticket.interprete_image: type param base64_image annoté bytes, mais on passe une str (base64 encodée). Harmoniser l’annotation.

6) interprete_lignes (carrefour/commun.py)
- En cas d’échec de parsing « q x pu », qte et pu peuvent ne pas être initialisés avant l’append, causant une UnboundLocalError.
- Action: définir qte=1 et pu=None par défaut avant le try.

7) Routers non exposés
- Dans main.py, seuls les endpoints Tickets sont inclus (app.include_router(ticket.router)).
- Action: inclure clients (et futurs: enseigne, produit_categorie) pour que l’API soit complète.

8) Redondance de schémas TicketInterprete
- Présence de modèles dans app/schemas/ticket_interprete.py et app/services/tickets/reconnaissance_tickets/model_ticket.py (doublon).
- Action: consolider pour éviter la dérive.

9) Nettoyage
- Imports inutilisés (ex: Session, select dans app/models/ticket.py).
- Action: nettoyage pour réduire l’empreinte et clarifier le code.

Améliorations envisageables:
- Réessayage (retry) avec backoff sur les appels OCR/catégorisation.
- Circuit breaker et timeouts.
- Tests d’intégration avec un OCR mocké (fixtures Markdown).
- Normalisation de la devise et formatage montant côté DTO.
- Ajout d’index DB et contraintes (NOT NULL/DEFAULT) selon les règles métiers.

Navigation:
- Qualité/Perf: [09 — Qualité & performances](./09_qualite_performance.md)
- Annexes: [11 — Annexes](./11_annexes.md)
- Retour pipeline: [04 — Pipeline d’ingestion](./04_pipeline_ingestion.md)

Voir aussi: [Sommaire](./00_navigation.md)