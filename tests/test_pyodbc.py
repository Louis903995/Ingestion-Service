import pyodbc

server = "simplon-certif.database.windows.net"  # ex: simplon-certif.database.windows.net
database = "simplon-certif"
username = "sqladminuser"
password = "LouisMoises123"
driver = "{ODBC Driver 18 for SQL Server}"
conn_str = f"Driver={driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# server = "localhost"
# database = "MaNouvelleBaseDeDonnees"
# username = "SA"
# password = "MotDePasseUltraFort123!"
# driver = "{ODBC Driver 18 for SQL Server}"
# conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;"

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 1. Créer la table client 
cursor.execute("""
IF OBJECT_ID('client', 'U') IS NULL
BEGIN
    CREATE TABLE client (
        client_id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(100) NOT NULL,
        prenom NVARCHAR(100) NOT NULL,
        email NVARCHAR(100) UNIQUE,
        budget DECIMAL(10,2) DEFAULT 0.00,
        date_creation DATETIME NOT NULL DEFAULT GETDATE(),
        date_modification DATETIME NOT NULL DEFAULT GETDATE()
    )
END
""")
conn.commit()
print("Table 'client' créée ou existe déjà.")

# Mise à jour automatique de date_modification sur client
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
        c.nom = ISNULL(i.nom, c.nom),
        c.prenom = ISNULL(i.prenom, c.prenom),
        c.email = ISNULL(i.email, c.email),
        c.budget = ISNULL(i.budget, c.budget),
        c.date_modification = CASE
            WHEN 
                (ISNULL(i.nom, c.nom) <> c.nom OR
                 ISNULL(i.prenom, c.prenom) <> c.prenom OR
                 ISNULL(i.email, c.email) <> c.email OR
                 ISNULL(i.budget, c.budget) <> c.budget)
            THEN GETDATE()
            ELSE c.date_modification
        END
    FROM client c
    INNER JOIN inserted i ON c.client_id = i.client_id;
END
""")
conn.commit()
print("Trigger 'trg_update_date_modification_client' créé.")

# 2. Créer la table supermarche
cursor.execute("""
IF OBJECT_ID('supermarche', 'U') IS NULL
BEGIN
    CREATE TABLE supermarche (
        supermarche_id INT PRIMARY KEY IDENTITY(1,1),
        magasin_nom NVARCHAR(200) NOT NULL,
        magasin_adresse NVARCHAR(300)
    )
END
""")
conn.commit()
print("Table 'supermarche' créée ou existe déjà.")


# 3. Créer la table ticket_entete
cursor.execute("""
IF OBJECT_ID('ticket_entete', 'U') IS NULL
BEGIN
    CREATE TABLE ticket_entete (
        ticket_id INT PRIMARY KEY IDENTITY(1,1),
        client_id INT NULL,
        date_heure_ticket DATETIME NOT NULL DEFAULT GETDATE(),
        supermarche_id INT NULL, 
        FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE SET NULL,
        FOREIGN KEY (supermarche_id) REFERENCES supermarche(supermarche_id)               
    )
END
""")
conn.commit()
print("Table 'ticket_entete' créée ou existe déjà.")


# 4. Créer la table categorie 
cursor.execute("""
IF OBJECT_ID('categorie', 'U') IS NULL
BEGIN
    CREATE TABLE categorie (
        categorie_id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(100) NOT NULL
    )
END
""")
conn.commit()
print("Table 'categorie' créée ou existe déjà.")


# 5. Créer la table ticket_ligne 
cursor.execute("""
IF OBJECT_ID('ticket_ligne', 'U') IS NULL
BEGIN
    CREATE TABLE ticket_ligne (
        ticket_ligne_id INT PRIMARY KEY IDENTITY(1,1),
        ticket_id INT NOT NULL,
        libelle NVARCHAR(100) NOT NULL,
        quantite INT NOT NULL DEFAULT 1,
        categorie_id INT NULL,
        prix_unitaire DECIMAL(10,2) NOT NULL,
        prix_total AS (quantite * prix_unitaire), -- colonne calculée
        FOREIGN KEY (ticket_id) REFERENCES ticket_entete(ticket_id) ON DELETE CASCADE,
        FOREIGN KEY (categorie_id) REFERENCES categorie(categorie_id)
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
