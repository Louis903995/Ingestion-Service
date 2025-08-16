IF NOT EXISTS (
    SELECT 1
FROM sys.schemas
WHERE name = 'achats'
)
BEGIN
    EXEC('CREATE SCHEMA achats');
END

IF NOT EXISTS (
    SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'achats' AND TABLE_NAME = 'Enseignes'
)
BEGIN
    CREATE TABLE achats.Enseignes
    (
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
    SELECT 1
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'achats' AND TABLE_NAME = 'ProduitCategories'
)
BEGIN
    CREATE TABLE achats.ProduitCategories
    (
        categorie_produit_id INT IDENTITY(1,1) PRIMARY KEY,
        nom_categorie_produit NVARCHAR(300) NOT NULL
    );
END

IF NOT EXISTS (
    SELECT 1
FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.name = 'TicketEntetes' AND s.name = 'achats'
)
BEGIN
    CREATE TABLE achats.TicketEntetes
    (
        ticket_id INT IDENTITY(1,1) PRIMARY KEY,
        client_id INT NOT NULL,
        date_heure_ticket DATETIME NOT NULL,
        enseigne_id INT NULL,
        montant_total_ticket DECIMAL(18, 2) NULL
    );
END

IF NOT EXISTS (
    SELECT 1
FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.name = 'TicketLignes' AND s.name = 'achats'
)
BEGIN
    CREATE TABLE achats.TicketLignes
    (
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