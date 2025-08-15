import pyodbc

server = "simplon-certif.database.windows.net"  
database = "simplon-certif"
username = "sqladminuser"
password = "LouisMoises123"
driver = "{ODBC Driver 18 for SQL Server}"
conn_str = f"Driver={driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 1. Créer la table client 
cursor.execute("""
IF OBJECT_ID('client', 'U') IS NULL
BEGIN
    CREATE TABLE client (
        client_id INT PRIMARY KEY IDENTITY(1,1),
        nom_client NVARCHAR(100) NOT NULL,
        prenom_client NVARCHAR(100) NOT NULL,
        email_client NVARCHAR(100) UNIQUE,
        adresse_client NVARCHAR(100) UNIQUE,               
        budget_client DECIMAL(10,2) DEFAULT 0.00,
        date_creation DATETIME NOT NULL DEFAULT GETDATE(),
        date_derniere_modification DATETIME NOT NULL DEFAULT GETDATE()
    )
END
""")
conn.commit()
print("Table 'client' créée ou existe déjà.")

# Mise à jour automatique de date_derniere_modification sur client
cursor.execute("""
IF OBJECT_ID('trg_update_date_modification_client', 'TR') IS NOT NULL
    DROP TRIGGER trg_update_date_modification_client;
""")
conn.commit()

cursor.execute("""
CREATE TRIGGER trg_prevent_manual_update_date_modification
ON client
INSTEAD OF UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- On ne met à jour que nom, prenom, email, budget
    UPDATE c
    SET
        c.nom_client = ISNULL(i.nom_client, c.nom_client),
        c.prenom_client = ISNULL(i.prenom_client, c.prenom_client),
        c.email_client = ISNULL(i.email_client, c.email_client),
        c.adresse_client = ISNULL(i.adresse_client, c.adresse_client),               
        c.budget_client = ISNULL(i.budget_client, c.budget_client),
        c.date_derniere_modification = CASE
            WHEN 
                (ISNULL(i.nom_client, c.nom_client) <> c.nom_client OR
                 ISNULL(i.prenom_client, c.prenom_client) <> c.prenom_client OR
                 ISNULL(i.email_client, c.email_client) <> c.email_client OR
                 ISNULL(i.adresse_client, c.adresse_client) <> c.adresse_client OR               
                 ISNULL(i.budget_client, c.budget_client) <> c.budget_client)
            THEN GETDATE()
            ELSE c.date_derniere_modification
        END
    FROM client c
    INNER JOIN inserted i ON c.client_id = i.client_id;
END
""")
conn.commit()
print("Trigger 'trg_update_date_modification_client' créé.")

# 2. Créer la table taille_enseigne
cursor.execute("""
IF OBJECT_ID('taille_enseigne', 'U') IS NULL
BEGIN
    CREATE TABLE taille_enseigne (
        taille_enseigne_id INT PRIMARY KEY IDENTITY(1,1),
        libelle_taille_enseigne NVARCHAR(100) NOT NULL UNIQUE
    )
END
""")
conn.commit()
print("Table 'taille_enseigne' créée ou existe déjà.")

# 3. Créer la table enseigne
cursor.execute("""
IF OBJECT_ID('enseigne', 'U') IS NULL
BEGIN
    CREATE TABLE enseigne (
        enseigne_id INT PRIMARY KEY IDENTITY(1,1),
        enseigne_nom NVARCHAR(200) NOT NULL,
        enseigne_adresse NVARCHAR(300),
        enseigne_num_tel_ticket NVARCHAR(300),
        taille_enseigne_id INT NULL
        FOREIGN KEY (taille_enseigne_id) REFERENCES taille_enseigne(taille_enseigne_id)               
    )
END
""")
conn.commit()
print("Table 'enseigne' créée ou existe déjà.")


# 4. Créer la table ticket_entete
cursor.execute("""
IF OBJECT_ID('ticket_entete', 'U') IS NULL
BEGIN
    CREATE TABLE ticket_entete (
        ticket_id INT PRIMARY KEY IDENTITY(1,1),
        client_id INT NULL,
        date_heure_ticket DATETIME NOT NULL DEFAULT GETDATE(),
        enseigne_id INT NULL,
        montant_total_ticket INT NULL, 
        FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE SET NULL,
        FOREIGN KEY (enseigne_id) REFERENCES enseigne(enseigne_id)               
    )
END
""")
conn.commit()
print("Table 'ticket_entete' créée ou existe déjà.")


# 5. Créer la table categorie_produit 
cursor.execute("""
IF OBJECT_ID('categorie_produit', 'U') IS NULL
BEGIN
    CREATE TABLE categorie_produit (
        categorie_produit_id INT PRIMARY KEY IDENTITY(1,1),
        nom_categorie_produit NVARCHAR(300)
    )
END
""")
conn.commit()
print("Table 'categorie_produit' créée ou existe déjà.")


# 6. Créer la table ticket_ligne 
cursor.execute("""
IF OBJECT_ID('ticket_ligne', 'U') IS NULL
BEGIN
    CREATE TABLE ticket_ligne (
        ticket_id INT NOT NULL,
        libelle_produit NVARCHAR(100) NOT NULL,
        quantite INT NOT NULL DEFAULT 1,
        categorie_produit_id INT NULL,
        prix_unitaire DECIMAL(10,2) NOT NULL,
        montant_total_ligne AS (quantite * prix_unitaire), -- colonne calculée
        FOREIGN KEY (ticket_id) REFERENCES ticket_entete(ticket_id) ON DELETE CASCADE,
        FOREIGN KEY (categorie_produit_id) REFERENCES categorie_produit(categorie_produit_id)
    )
END
""")
conn.commit()
print("Table 'ticket_ligne' créée ou existe déjà.")


# Vérifier les tables existantes
cursor.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
""")

tables = cursor.fetchall()
print("\nTables existantes dans la base :")
for table in tables:
    print(f"- {table[0]}")
