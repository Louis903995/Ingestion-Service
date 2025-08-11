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
cursor.execute(
"""
IF OBJECT_ID('client', 'U') IS NULL
CREATE TABLE client (
    client_id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(100),
    prenom NVARCHAR(100),
    budget DECIMAL(10,2),
    date_enregistrement DATETIME
)
"""
)
conn.commit()
print("Table 'client' créée ou existe déjà.")

# 2. Créer la table ticket 
cursor.execute(
"""
IF OBJECT_ID('ticket', 'U') IS NULL
CREATE TABLE ticket (
    id_ticket INT PRIMARY KEY IDENTITY(1,1),
    client_id INT,
    libelle NVARCHAR(255),
    FOREIGN KEY (client_id) REFERENCES client(client_id)
)
"""
)
conn.commit()
print("Table 'ticket' créée ou existe déjà.")

# 3. Créer la table categorie
cursor.execute(
"""
IF OBJECT_ID('categorie', 'U') IS NULL
CREATE TABLE categorie (
    id_cat INT PRIMARY KEY IDENTITY(1,1),
    id_ticket INT,
    libelle NVARCHAR(100),
    categorie NVARCHAR(50)
)
"""
)
conn.commit()
print("Table 'categorie' créée ou existe déjà.")

# 4. Créer la table categorie_produits
cursor.execute(
"""
IF OBJECT_ID('categorie_produits', 'U') IS NULL
CREATE TABLE categorie_produits (
    id INT PRIMARY KEY IDENTITY(1,1),
    libelle NVARCHAR(100),
    categorie NVARCHAR(100),
    created_at DATETIME
)
"""
)
conn.commit()
print("Table 'categorie_produits' créée ou existe déjà.")

# 5. Créer la table supermarche
cursor.execute(
"""
IF OBJECT_ID('supermarche', 'U') IS NULL
CREATE TABLE supermarche (
    id_supermarche INT PRIMARY KEY IDENTITY(1,1),
    id_ticket INT,
    nom_magasin NVARCHAR(100),
    date_achat DATETIME,
    prix_total DECIMAL(10,2)
)
"""
)
conn.commit()
print("Table 'supermarche' créée ou existe déjà.")

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




# Exemple de data 

# Insérer une ligne dans la table client
cursor.execute("INSERT INTO client (nom, prenom, budget, date_enregistrement) VALUES (?, ?, ?, ?)", ("Dupont", "Victor", 200, "06/06/2018"))
conn.commit()

# Insérer une ligne dans la table ticket
cursor.execute("INSERT INTO ticket (client_id, libelle) VALUES (?, ?)", (1, "coca-cola"))
conn.commit()

# Insérer une ligne dans la table categorie
cursor.execute("INSERT INTO categorie (id_ticket, libelle, categorie) VALUES (?, ?, ?)", (1, "coca_cola", "boissons"))
conn.commit()

# Insérer une ligne dans la table categorie_produits
#cursor.execute("INSERT INTO categorie_produits (libelle, categorie, created_at) VALUES (?, ?, ?)", ())
#conn.commit()

# Insérer une ligne dans la table supermarche
cursor.execute("INSERT INTO supermarche (id_ticket, nom_magasin, date_achat, prix_total) VALUES (?, ?, ?, ?)", (1, "Carrefour", "10/08/2025", 200))
conn.commit()

cursor.close()
conn.close()