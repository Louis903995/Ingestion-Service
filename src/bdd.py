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


IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'achats' AND TABLE_NAME = 'ProduitCategories'
)
BEGIN
    CREATE TABLE achats.ProduitCategories (
        categorie_produit_id INT IDENTITY(1,1) PRIMARY KEY,
        nom_categorie_produit NVARCHAR(300) NOT NULL
    );
END

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE t.name = 'TicketEntetes' AND s.name = 'achats'
)
BEGIN
    CREATE TABLE achats.TicketEntetes (
        ticket_id INT IDENTITY(1,1) PRIMARY KEY,
        client_id INT NOT NULL,
        date_heure_ticket DATETIME NOT NULL,
        enseigne_id INT NULL,
        montant_total_ticket DECIMAL(18, 2) NULL
    );
END


IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE t.name = 'TicketLignes' AND s.name = 'achats'
)
BEGIN
    CREATE TABLE achats.TicketLignes (
        ticket_ligne_id INT IDENTITY(1,1) PRIMARY KEY,
        ticket_id INT NOT NULL,
        libelle_produit NVARCHAR(100) NOT NULL,
        quantite INT NOT NULL DEFAULT 1,
        categorie_produit_id INT NULL,
        prix_unitaire DECIMAL(18,2) NULL,
        montant_total_ligne DECIMAL(18,2) NULL,
        CONSTRAINT FK_TicketLignes_TicketEntetes
            FOREIGN KEY (ticket_id) REFERENCES achats.TicketEntetes(ticket_id),
        CONSTRAINT FK_TicketLignes_ProduitCategories
            FOREIGN KEY (categorie_produit_id) REFERENCES achats.ProduitCategories(categorie_produit_id)
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
# https://www.insee.fr/fr/statistiques/1281004
"""

INSERT INTO achats.ProduitCategories (nom_categorie_produit) VALUES 
(N'Fruits & légumes'),
(N'Viandes & poissons'),
(N'Produits laitiers'),
(N'Épicerie salée'),
(N'Épicerie sucrée'),
(N'Surgelés'),
(N'Frais'),
(N'Eaux'),
(N'Boissons alcoolisées'),
(N'Boissons non alcoolisées (hors eaux)');

-------------------------------------------------------------

INSERT INTO achats.Enseignes (
        enseigne_nom,
        enseigne_adresse,
        categorie_enseigne,
        enseigne_surface_m2,
        enseigne_num_tel_ticket,
        enseigne_nom_ticket
)
VALUES
    (N'Carrefour Market Baisieux', N'31 Avenue D''Ogimont 59780 Baisieux', 'SUPERMARCHE', 1800, '0320419428', N'MARKET BAISIEUX'),
    (N'Carrefour City Chéreng', N'81 ROUTE NATIONALE 59152 CHERENG', 'SUPERETTE', 350, '0320790662', N'SARL AJ.DISTRI 81 ROUTE NATIONALE 59152 CHERENG'),
    (N'Intermarché Express Lille', N'12 Rue de la Gare 59800 Lille', 'SUPERETTE', 400, '0320567890', N'INTERMARCHE EXPRESS LILLE'),
    (N'Auchan Drive Villeneuve', N'5 Avenue du Pont de Bois 59650 Villeneuve-d''Ascq', 'DRIVE', 1200, '0320456789', N'AUCHAN DRIVE VILLENEUVE'),
    (N'Leclerc Wattrelos', N'99 Rue Carnot 59150 Wattrelos', 'HYPERMARCHE', 3500, '0320789456', N'LECLERC WATTRELOS');

INSERT INTO achats.TicketEntetes (client_id, date_heure_ticket, enseigne_id, montant_total_ticket) VALUES
(1, '2025-08-01 10:23:00', 1, 12.60),
(1, '2025-08-02 18:41:00', 2, 21.50),
(1, '2025-08-03 09:01:00', 1, 7.50),
(1, '2025-08-05 13:12:00', 3, 16.30),
(1, '2025-08-10 15:55:00', 2, 9.90),
(2, '2025-08-01 09:56:00', 1, 13.40),
(2, '2025-08-04 14:15:00', 2, 17.90),
(2, '2025-08-08 18:31:00', 3, 8.10),
(2, '2025-08-12 10:10:00', 2, 25.50),
(2, '2025-08-13 17:44:00', 1, 14.30),
(2, '2025-08-15 16:21:00', 3, 19.20),
(3, '2025-08-02 12:05:00', 1, 15.70),
(3, '2025-08-08 11:22:00', 2, 17.30),
(3, '2025-08-11 09:00:00', 1, 12.90),
(3, '2025-08-15 18:55:00', 2, 22.10),
(3, '2025-08-16 13:11:00', 3, 13.60);

INSERT INTO achats.TicketLignes (ticket_id, libelle_produit, quantite, categorie_produit_id, prix_unitaire, montant_total_ligne) VALUES
(1, N'Pomme', 2, 1, 1.10, 2.20),
(1, N'Jambon', 1, 2, 2.40, 2.40),
(1, N'Bouteille Eau', DEFAULT, 8, DEFAULT, DEFAULT),
(2, N'Camembert', 1, 3, 2.70, 2.70),
(2, N'Biscottes', 1, 4, DEFAULT, DEFAULT),
(2, N'Jus d''orange', 2, 9, 1.50, 3.00),
(2, N'Barres chocolatées', DEFAULT, DEFAULT, DEFAULT, DEFAULT),
(3, N'Poulet', 1, 2, 5.10, 5.10),
(3, N'Pain', DEFAULT, DEFAULT, DEFAULT, DEFAULT),
(4, N'Yaourt nature', 4, 3, 0.60, 2.40),
(4, N'Compote', 2, DEFAULT, 0.75, 1.50),
(5, N'Bière', DEFAULT, 9, 2.90, DEFAULT),
(5, N'Pain de mie', DEFAULT, DEFAULT, DEFAULT, DEFAULT),
(6, N'Carottes', 3, 1, 0.90, 2.70),
(6, N'Riz', 1, 4, 1.30, 1.30),
(7, N'Vin rouge', DEFAULT, 9, 6.50, DEFAULT),
(7, N'Glace', 2, 6, 2.10, 4.20),
(7, N'Chips', 1, 4, DEFAULT, DEFAULT),
(8, N'Pommes', 5, 1, 0.80, 4.00),
(9, N'Filet de poisson', 1, 2, 5.90, 5.90),
(9, N'Pâtes', 2, 4, 1.20, 2.40),
(9, N'Brioche', DEFAULT, DEFAULT, DEFAULT, DEFAULT),
(10, N'Yaourt nature', 6, 3, 0.50, 3.00),
(10, N'Salade', 1, 1, 1.10, 1.10),
(10, N'Tomates', DEFAULT, 1, DEFAULT, DEFAULT),
(11, N'Poulet rôti', DEFAULT, 2, 9.90, DEFAULT),
(11, N'Pain complet', 1, DEFAULT, 1.10, 1.10),
(12, N'Bananes', 4, 1, 0.75, 3.00),
(12, N'Jambon blanc', 1, 2, 2.90, 2.90),
(13, N'Fromage râpé', 2, 3, 1.50, 3.00),
(13, N'Pizza surgelée', 1, 6, 4.90, 4.90),
(13, N'Bière', DEFAULT, 9, DEFAULT, DEFAULT),
(14, N'Croissants', 3, 5, 0.90, 2.70),
(14, N'Pain', DEFAULT, DEFAULT, DEFAULT, DEFAULT),
(15, N'Beurre', 1, 3, 2.30, 2.30),
(15, N'Rillettes', 1, 4, DEFAULT, DEFAULT),
(16, N'Chocolat', 2, 5, 1.00, 2.00),
(16, N'Jus de pomme', DEFAULT, 9, DEFAULT, DEFAULT);

"""

"""
-- drop Enseignes 
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.Enseignes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.Enseignes;
GO

-- drop ProductCategories 
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.ProduitCategories');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.ProduitCategories;
GO

-- drop TicketEntetes
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.TicketEntetes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.TicketEntetes;
GO

-- drop TicketLignes
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.TicketLignes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.TicketLignes;
GO

DROP SCHEMA IF EXISTS achats;
GO
"""
