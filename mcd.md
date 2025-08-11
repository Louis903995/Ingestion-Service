# MCD - Base de données Supermarché

```mermaid
erDiagram
    CLIENT {
        int client_id PK
        nvarchar nom
        nvarchar prenom
        decimal budget
        datetime date_enregistrement
    }
    
    TICKET {
        int id_ticket PK
        int client_id FK
        nvarchar libelle
    }
    
    CATEGORIE {
        int id_cat PK
        int id_ticket FK
        nvarchar libelle
        nvarchar categorie
    }
    
    SUPERMARCHE {
        int id_supermarche PK
        int id_ticket FK
        nvarchar nom_magasin
        datetime date_achat
        decimal prix_total
    }
    
    CATEGORIE_PRODUITS {
        int id PK
        nvarchar libelle
        nvarchar categorie
        datetime created_at
    }
    
    CLIENT ||--o{ TICKET : "possède"
    TICKET ||--o{ CATEGORIE : "contient"
    TICKET ||--o{ SUPERMARCHE : "émis par"