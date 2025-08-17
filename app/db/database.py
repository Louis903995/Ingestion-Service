# db/database.py
from sqlmodel import SQLModel, create_engine, Session
import os

SERVER = os.getenv("DB_SERVER")
PORT = os.getenv("DB_PORT", "1433")
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}"
    f"?driver={DRIVER.replace(' ', '+')}&TrustServerCertificate=yes"
)

# Création de l'engine SQLModel
engine = create_engine(DATABASE_URL, echo=True, future=True)


def create_db_and_tables():
    """Créer les tables à partir des modèles SQLModel"""
    SQLModel.metadata.create_all(engine)


# Dependency à utiliser dans FastAPI (ou tes services)
def get_session():
    with Session(engine) as session:
        yield session
