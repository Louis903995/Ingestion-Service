# db/database.py
import logging
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=".env", override=False)

PORT = os.getenv("DB_PORT", "1433")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
TRUST_SERVER_CERTIFICATE = (
    "yes" if os.getenv("TRUST_SERVER_CERTIFICATE", "no").lower() == "yes" else "no"
)

DATABASE_URL = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{PORT}/{os.getenv('DB_NAME')}"
    f"?driver={DRIVER.replace(' ', '+')}&TrustServerCertificate={TRUST_SERVER_CERTIFICATE}"
)

# Création de l'engine SQLModel
try:
    engine = create_engine(DATABASE_URL, echo=True, future=True)
except Exception as e:
    logger.critical(f"Impossible de créer la db, {e}")


# def create_db_and_tables():
#     """Créer les tables à partir des modèles SQLModel"""
#     SQLModel.metadata.create_all(engine)


# Dependency à utiliser dans FastAPI (ou tes services)
def get_session():
    with Session(engine) as session:
        yield session
