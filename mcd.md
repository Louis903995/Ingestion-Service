## MCD - Système de gestion des tickets

```mermaid
erDiagram
    client {
        INT client_id PK
        NVARCHAR nom_client
        NVARCHAR prenom_client
        NVARCHAR email_client
        NVARCHAR adresse_client
        DECIMAL budget_client
        DATETIME date_creation
        DATETIME date_derniere_modification
    }

    taille_enseigne {
        INT taille_enseigne_id PK
        NVARCHAR libelle_taille_enseigne
    }

    enseigne {
        INT enseigne_id PK
        NVARCHAR enseigne_nom
        NVARCHAR enseigne_adresse
        NVARCHAR enseigne_num_tel_ticket
        INT taille_enseigne_id FK
    }

    ticket_entete {
        INT ticket_id PK
        INT client_id FK
        DATETIME date_heure_ticket
        INT enseigne_id FK
        INT montant_total_ticket
    }

    categorie_produit {
        INT categorie_produit_id PK
        NVARCHAR nom_categorie_produit
    }

    ticket_ligne {
        INT ticket_id FK
        NVARCHAR libelle_produit
        INT quantite
        INT categorie_produit_id FK
        DECIMAL prix_unitaire
        DECIMAL montant_total_ligne
    }

    client ||--o{ ticket_entete : génère
    enseigne ||--o{ ticket_entete : émet
    taille_enseigne ||--o{ enseigne : définit
    ticket_entete ||--|{ ticket_ligne : contient
    categorie_produit ||--o{ ticket_ligne : classifie
