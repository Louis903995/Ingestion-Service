```mermaid
%%{init: {"theme": "base"}}%%
erDiagram
    CLIENT {
        int client_id PK
        nvarchar nom
        nvarchar prenom
        nvarchar email
        decimal budget
        datetime date_creation
        datetime date_modification
    }

    SUPERMARCHE {
        int supermarche_id PK
        nvarchar supermarche_nom
        nvarchar supermarche_adresse
    }

    TICKET_ENTETE {
        int ticket_id PK
        int client_id FK
        datetime date_heure_ticket
        int supermarche_id FK
    }

    CATEGORIE {
        int categorie_id PK
        nvarchar nom
    }

    TICKET_LIGNE {
        int ticket_id FK
        nvarchar libelle
        int quantite
        int categorie_id FK
        decimal prix_unitaire
        decimal prix_total
    }

    CLIENT ||--o{ TICKET_ENTETE : client_id ON DELETE SET NULL
    SUPERMARCHE ||--o{ TICKET_ENTETE : supermarche_id
    TICKET_ENTETE ||--o{ TICKET_LIGNE : ticket_id ON DELETE CASCADE
    CATEGORIE ||--o{ TICKET_LIGNE : categorie_id


```
