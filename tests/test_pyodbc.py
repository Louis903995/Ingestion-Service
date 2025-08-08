import pyodbc


# server = "simplon-certif.database.windows.net"  # ex: simplon-certif.database.windows.net
# database = "simplon-certif"
# username = "sqladminuser"
# password = "LouisMoises123"
# driver = "{ODBC Driver 18 for SQL Server}"
# conn_str = f"Driver={driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


server = "localhost"
database = "MaNouvelleBaseDeDonnees"
username = "SA"
password = "MotDePasseUltraFort123!"
driver = "{ODBC Driver 18 for SQL Server}"
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;"


conn = pyodbc.connect(conn_str)
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
