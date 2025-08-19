# 03 — Modélisation: SQLModel vs BaseModel

Pourquoi deux familles de modèles ?
- SQLModel (hérite de Pydantic + SQLAlchemy) pour les entités persistées et leurs relations.
- BaseModel Pydantic pour les objets d’échange transitoires (entrée/sortie API, modèles intermédiaires non stockés tels que les tickets interprétés issus de l’OCR).

Exemples SQLModel (persistés):
- app/models/ticket.py: TicketEntete, TicketLignes
- app/models/enseigne.py: Enseigne
- app/models/produit_categorie.py: ProduitCategorie
- app/models/client.py: Client

Exemples BaseModel/DTO (transitoires):
- app/schemas/ticket_interprete.py: TicketInterprete, LigneTicketInterpretee (résultat parsing OCR)
- app/schemas/ticket_reponse.py: TicketEnteteResponse, TicketLigneResponse (réponses API)
- app/schemas/client.py: ClientCreate, ClientUpdate (payloads)

Avantages:
- SQLModel: relations, contraintes, cohérence avec la base, type-safety.
- BaseModel: validation d’entrée/sortie, contrôle strict des contrats API, dissociation des schémas de transport et des entités persistées.

Diagramme de classes (simplifié, côté SQLModel):

```mermaid
classDiagram
  class TicketEntete {
    +ticket_id: int
    +client_id: int
    +date_heure_ticket: datetime
    +enseigne_id: int
    +montant_total_ticket: float
  }
  class TicketLignes {
    +ticket_ligne_id: int
    +ticket_id: int
    +libelle_produit: str
    +quantite: int
    +categorie_produit_id: int
    +prix_unitaire: float?
    +montant_total_ligne: float
    +nom_categorie_produit(): str?
  }
  class ProduitCategorie {
    +categorie_produit_id: int
    +nom_categorie_produit: str
  }
  class Enseigne {
    +enseigne_id: int
    +enseigne_nom: str
    +enseigne_adresse: str
    +enseigne_surface_m2: int
    +enseigne_num_tel_ticket: str
    +enseigne_nom_ticket: str
  }
  class Client {
    +client_id: int
    +nom_client: str
    +prenom_client: str
    +email_client: str?
    +adresse_client: str?
    +budget_client: float
  }

  TicketEntete "1" --> "many" TicketLignes
  TicketEntete "1" --> "1" Enseigne
  TicketEntete "1" --> "1" Client
  TicketLignes "many" --> "1" ProduitCategorie
```

Remarques importantes:
- Propriété calculée nom_categorie_produit dans TicketLignes s’appuie sur la relation catégorie.
- Les modèles Update (TicketEnteteUpdate, TicketLignesUpdate) lèvent une exception en __init__ pour interdire toute modification post création (invariants métiers).

Navigation:
- Pipeline: [04 — Pipeline d’ingestion](./04_pipeline_ingestion.md)
- Parsing: [05 — Parsing par enseigne](./05_parsing_enseignes.md)
- Services: [06 — Services métiers](./06_services_metier.md)

Voir aussi: [Sommaire](./00_navigation.md)