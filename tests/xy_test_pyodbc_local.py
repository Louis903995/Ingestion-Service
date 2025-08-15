import pyodbc

# Remplacez les valeurs par celles correspondant à votre configuration
server = "sqlserver-dev"
# server = "localhost"
database = "master"  # Connexion initiale à la base de données master
username = "SA"
password = "MotDePasseUltraFort123!"
driver = "{ODBC Driver 18 for SQL Server}"

conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;"

try:
    # Établissez la connexion
    print("------------------------------------------------")
    conn = pyodbc.connect(conn_str)
    conn.autocommit = True  # Active le mode autocommit pour éviter les transactions multi-instructions
    cursor = conn.cursor()

    # Nom de la base de données à vérifier/créer
    db_name = "MaNouvelleBaseDeDonnees"

    # Vérifiez si la base de données existe déjà
    cursor.execute(f"SELECT 1 FROM sys.databases WHERE name = '{db_name}'")
    if not cursor.fetchone():
        # Si la base de données n'existe pas, créez-la
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"La base de données {db_name} a été créée avec succès.")
    else:
        print(
            f"La base de données {db_name} existe déjà. Aucune action n'est nécessaire."
        )

except pyodbc.Error as e:
    print(f"Erreur lors de l'opération sur la base de données: {e}")

finally:
    # Fermez la connexion
    if "conn" in locals():
        conn.close()
        print ("--- Connection closed")

database = "MaNouvelleBaseDeDonnees"
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;"


print ("----------------------------------")
conn = pyodbc.connect(conn_str)
print ("----------------------------------")
cursor = conn.cursor()

# 1. Créer une table
cursor.execute(
    """
    IF OBJECT_ID('personnes', 'U') IS NULL
    CREATE TABLE personnes (
        id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(50),
        age INT
    )
"""
)
conn.commit()
print ("----------------------------------")
# 2. Insérer une ligne
cursor.execute("INSERT INTO personnes (nom, age) VALUES (?, ?)", ("Alice", 30))
conn.commit()

# 3. Lire les données
cursor.execute("SELECT * FROM personnes")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
