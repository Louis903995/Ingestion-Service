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

#1. Créer la table categories
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


# 2. Créer la table categorie_produits
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


# 3. Créer la table client
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


#4. Créer la table supermarche
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


# 5. Créer la table ticket 
cursor.execute(
    """
    IF OBJECT_ID('ticket', 'U') IS NULL
    CREATE TABLE ticket (
        id_ticket INT PRIMARY KEY IDENTITY(1,1),
        client_id INT FOREIGN KEY REFERENCES client(client_id),
        libelle NVARCHAR(255)
    )
    """
)
conn.commit()

# 2. Insérer une ligne
#cursor.execute("INSERT INTO personnes (nom, age) VALUES (?, ?)", ("Alice", 30))
#conn.commit()

# 3. Lire les données
cursor.execute("SELECT * FROM personnes")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
