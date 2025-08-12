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
CREATE TRIGGER trg_update_date_modification_client
ON client
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE client
    SET date_modification = GETDATE()
    FROM inserted i
    WHERE client.client_id = i.client_id;
END
""")
conn.commit()
print("Trigger 'trg_update_date_modification_client' créé.")


# 2. Créer la table ticket_entete
cursor.execute("""
IF OBJECT_ID('ticket_entete', 'U') IS NULL
BEGIN
    CREATE TABLE ticket_entete (
        ticket_id INT PRIMARY KEY IDENTITY(1,1),
        client_id INT NULL,
        date_heure_ticket DATETIME NOT NULL DEFAULT GETDATE(),
        magasin_nom NVARCHAR(200) NOT NULL,
        magasin_adresse NVARCHAR(300),
        FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE SET NULL
    )
END
""")
conn.commit()
print("Table 'ticket_entete' créée ou existe déjà.")


# 3. Créer la table correspondance 
cursor.execute("""
IF OBJECT_ID('correspondance', 'U') IS NULL
BEGIN
    CREATE TABLE correspondance (
        categorie_id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(100) NOT NULL
    )
END
""")
conn.commit()
print("Table 'correspondance' créée ou existe déjà.")


# 4. Créer la table ticket_ligne 
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
        FOREIGN KEY (categorie_id) REFERENCES correspondance(categorie_id)
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
