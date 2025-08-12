from sqlmodel import create_engine, Session

# Connexion à la base Azure SQL
server = "simplon-certif.database.windows.net"
database = "simplon-certif"
username = "sqladminuser"
password = "LouisMoises123"
driver = "ODBC Driver 18 for SQL Server"

DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver.replace(' ', '+')}"

engine = create_engine(DATABASE_URL, echo=True)

# Dépendance pour avoir une session DB
def get_session():
    with Session(engine) as session:
        yield session