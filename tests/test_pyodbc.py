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


"""
# Supprimer toutes les données des tables 
cursor.execute("DELETE FROM supermarche")
cursor.execute("DELETE FROM categorie")
cursor.execute("DELETE FROM ticket")
cursor.execute("DELETE FROM client")
conn.commit()

# Réinitialiser le compteur d'auto-incrément (IDENTITY) à 0 pour chaque table
# Cela garantit que les prochaines insertions repartiront de 1 et qu'en executant ce script 2 fois, on aura 2 fois les mêmes données 
cursor.execute("DBCC CHECKIDENT ('supermarche', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('categorie', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('ticket', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('client', RESEED, 0)")
conn.commit()
"""


### Exemple de data

# Insérer les clients et récupérer leurs IDs
clients_data = [
    ("Dupont", "Victor", 200, "2018-06-06"),
    ("Martin", "Sophie", 300, "2018-06-06"),
    ("Lemoine", "Claire", 150, "2018-06-06"),
    ("Moises", "Louis", 162, "2018-06-06"),
    ("Brad", "Pitt", 89, "2018-06-06")
]

client_ids = []
for client in clients_data:
    cursor.execute("""
        INSERT INTO client (nom, prenom, budget, date_enregistrement)
        OUTPUT INSERTED.client_id
        VALUES (?, ?, ?, ?)
    """, client)
    client_ids.append(cursor.fetchone()[0])
conn.commit()

# Insérer les tickets liés aux bons client_id
tickets_data = [
    (client_ids[0], "coca-cola"),
    (client_ids[1], "steaks hachés"),
    (client_ids[2], "eau"),
    (client_ids[3], "maltesers"),
    (client_ids[4], "frites")
]

ticket_ids = []
for ticket in tickets_data:
    cursor.execute("""
        INSERT INTO ticket (client_id, libelle)
        OUTPUT INSERTED.id_ticket
        VALUES (?, ?)
    """, ticket)
    ticket_ids.append(cursor.fetchone()[0])
conn.commit()

# Insérer les catégories liées aux bons id_ticket
categorie_data = [
    (ticket_ids[0], "Coca-Cola", "boissons"),
    (ticket_ids[1], "steaks hachés", "viandes et charcuterie"),
    (ticket_ids[2], "eau", "eau"),
    (ticket_ids[3], "Maltesers", "épicerie sucrée"),
    (ticket_ids[4], "frites", "surgelés")
]
cursor.executemany("""
    INSERT INTO categorie (id_ticket, libelle, categorie)
    VALUES (?, ?, ?)
""", categorie_data)
conn.commit()

# Insérer les supermarchés liés aux bons id_ticket
supermarche_data = [
    (ticket_ids[0], "Carrefour", "2018-06-06", 200),
    (ticket_ids[1], "Aldi", "2018-06-06", 300),
    (ticket_ids[2], "Auchan", "2018-06-06", 400),
    (ticket_ids[3], "Lidl", "2018-06-06", 600),
    (ticket_ids[4], "Carrefour", "2018-06-06", 200)
]
cursor.executemany("""
    INSERT INTO supermarche (id_ticket, nom_magasin, date_achat, prix_total)
    VALUES (?, ?, ?, ?)
""", supermarche_data)
conn.commit()

cursor.close()
conn.close()
