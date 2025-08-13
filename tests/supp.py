import pyodbc

"""
Script servant à supprimer les tables de la bdd hébergée sur Azure, pour en recréer d'autres
"""

server = "simplon-certif.database.windows.net"  # ex: simplon-certif.database.windows.net
database = "simplon-certif"
username = "sqladminuser"
password = "LouisMoises123"
driver = "{ODBC Driver 18 for SQL Server}"
conn_str = f"Driver={driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("""
DECLARE @sql NVARCHAR(MAX) = N'';

SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id)) + '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) + 
              ' DROP CONSTRAINT ' + QUOTENAME(name) + ';' + CHAR(13)
FROM sys.foreign_keys;

EXEC sp_executesql @sql;

DECLARE @sqlDropTables NVARCHAR(MAX) = N'';

SELECT @sqlDropTables += 'DROP TABLE ' + QUOTENAME(SCHEMA_NAME(schema_id)) + '.' + QUOTENAME(name) + ';' + CHAR(13)
FROM sys.tables;

EXEC sp_executesql @sqlDropTables;
""")
conn.commit()
