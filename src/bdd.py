import sqlite3


def creer_base_donnees():
    """
    Crée la base de données SQLite avec toutes les tables
    """
    # Créer ou ouvrir la base de données SQLite

    # Créer ou ouvrir la base de données SQLite
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    # Table Clients
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            budget REAL,
            date_enregistrement DATE
        )
    """
    )

    # Table Tickets
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tickets (
            id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            libelle TEXT
        )
    """
    )

    # Table Categories
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Categories (
            id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ticket INTEGER,
            libelle TEXT,
            categorie TEXT
        )
    """
    )

    cursor.execute(
        """
IF NOT EXISTS (
    SELECT 1 FROM sys.schemas WHERE name = 'achats'
)
BEGIN
    EXEC('CREATE SCHEMA achats');
END

IF NOT EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'achats' AND TABLE_NAME = 'Enseignes'
)
BEGIN
    CREATE TABLE achats.Enseignes (
        enseigne_id INT IDENTITY(1,1) PRIMARY KEY,
        enseigne_nom NVARCHAR(200) NOT NULL,
        enseigne_adresse NVARCHAR(300) NULL,
        categorie_enseigne NVARCHAR(20) NULL,
        enseigne_surface_m2 INT DEFAULT 0,
        enseigne_num_tel_ticket NVARCHAR(300) NULL,
        enseigne_nom_ticket NVARCHAR(200) NULL
    );
END          
    """
    )

    # Valider les changements
    conn.commit()

    # Fermer proprement la connexion
    conn.close()


if __name__ == "__main__":
    creer_base_donnees()

# Au sein de l'alimentaire non spécialisé, les hypermarchés ont une surface de 2 500 m² et plus, '
# les supermarchés de 400 à moins de 2 500 m², les supérettes de 120 à moins de 400 m² et les commerces d'alimentation générale de moins de 120 m².
# https://www.insee.fr/fr/statistiques/1281004
"""
INSERT INTO achats.Enseignes (
        enseigne_nom,
        enseigne_adresse,
        categorie_enseigne,
        enseigne_surface_m2,
        enseigne_num_tel_ticket,
        enseigne_nom_ticket
)
VALUES
    ('Carrefour Market Baisieux', '31 Avenue D''Ogimont 59780 Baisieux', 'SUPERMARCHE', 1800, '0320419428', 'MARKET BAISIEUX'),
    ('Carrefour City Chéreng', '81 ROUTE NATIONALE 59152 CHERENG', 'SUPERETTE', 350, '0320790662', 'SARL AJ.DISTRI 81 ROUTE NATIONALE 59152 CHERENG'),
    ('Intermarché Express Lille', '12 Rue de la Gare 59800 Lille', 'SUPERETTE', 400, '0320567890', 'INTERMARCHE EXPRESS LILLE'),
    ('Auchan Drive Villeneuve', '5 Avenue du Pont de Bois 59650 Villeneuve-d''Ascq', 'DRIVE', 1200, '0320456789', 'AUCHAN DRIVE VILLENEUVE'),
    ('Leclerc Wattrelos', '99 Rue Carnot 59150 Wattrelos', 'HYPERMARCHE', 3500, '0320789456', 'LECLERC WATTRELOS');
"""