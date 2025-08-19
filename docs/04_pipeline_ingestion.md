# 04 — Pipeline d’ingestion de tickets

Rôles principaux:
- OCR via Mistral (mistralai) pour obtenir un Markdown lisible.
- Sélection de la stratégie de parsing selon l’enseigne (resolver).
- Enrichissement:
  - Catégorisation des produits via microservice externe.
  - Résolution de l’enseigne (id) via matching flou.
- Persistence (entête + lignes) en base.

Code concerné:
- app/services/tickets/ingestion_ticket.py
- app/services/tickets/reconnaissance_tickets/resolver.py
- app/services/tickets/reconnaissance_tickets/enseignes/carrefour/*
- app/services/ticket_service.py (orchestration de la persistance)
- app/metrics.py (suivi erreurs/succès)

Séquence détaillée:

```mermaid
sequenceDiagram
  participant User
  participant Router as Router /tickets
  participant TicketSrv as TicketService
  participant Ingest as ingestion_ticket
  participant OCR as Mistral OCR
  participant Cat as Microservice Catégorisation
  participant DB as SQL Server

  User->>Router: POST /clients/{id}/tickets (Upload image)
  Router->>TicketSrv: ingere_image(session, client_id, base64_image)
  TicketSrv->>Ingest: ingere_image(client_id, base64_image)
  Ingest->>OCR: process(image data URL)
  OCR-->>Ingest: markdown + pages
  Ingest->>Ingest: resolver.extrait_ticket_scanne(markdown)
  Ingest->>Cat: POST /predict {produits: [libellés]}
  Cat-->>Ingest: catégories par produit
  Ingest->>Ingest: mapping catégories -> ids (cache RAM)
  Ingest->>Ingest: EnseigneService.trouve_enseigne_id(...)
  Ingest-->>TicketSrv: TicketInterprete enrichi
  TicketSrv->>DB: INSERT TicketEntete + TicketLignes
  TicketSrv-->>Router: TicketEnteteResponse
  Router-->>User: 200 OK (ticket enregistré)
```

Gestion des erreurs:
- Compteurs OpenTelemetry (COMPTEUR_INGESTIONS_TICKET_ERREUR) incrémentés avec étiquettes: OCR impossible, catégorisation impossible, résolution enseigne impossible.
- COMPTEUR_TOTAL_INGESTIONS_TICKET compte les succès/échecs globaux.

Navigation:
- Parsing enseignes: [05 — Parsing par enseigne](./05_parsing_enseignes.md)
- Services: [06 — Services métiers](./06_services_metier.md)
- API: [07 — API et routes](./07_api_endpoints.md)

Voir aussi: [Sommaire](./00_navigation.md)