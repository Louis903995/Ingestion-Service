# Focus — Diagrammes ciblés (sélection complémentaire)

Composants ingestion:

```mermaid
graph LR
  Upload[Upload Image] --> RouterTickets
  RouterTickets --> TicketService
  TicketService --> IngestionTicket
  IngestionTicket --> OCR[Mistral OCR]
  IngestionTicket --> Categorisation[Service Catégorisation]
  IngestionTicket --> EnseigneService
  EnseigneService --> DicoEnseignes[(Cache en mémoire)]
  IngestionTicket --> DicoCategories[(Cache catégories)]
  TicketService --> DB[(SQL Server)]
```

Séquence récupération tickets et lignes:

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Svc as TicketService
  participant DB

  Client->>API: GET /clients/{id}/tickets
  API->>Svc: get_tickets(session, client_id, dates)
  Svc->>DB: SELECT TicketEntete WHERE client_id + dates
  DB-->>Svc: liste tickets
  Svc->>DB: SELECT TicketLignes (selectinload categorie)
  DB-->>Svc: lignes + catégories
  Svc-->>API: [TicketEnteteResponse]
  API-->>Client: 200 OK
```

Voir:
- Pipeline: [04 — Pipeline d’ingestion](./04_pipeline_ingestion.md)
- Services: [06 — Services métiers](./06_services_metier.md)