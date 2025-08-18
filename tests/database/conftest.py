from dotenv import load_dotenv
import pytest
import logging
import os

from sqlmodel import Session, create_engine

from tests.pyodbc_utils import (
    cree_database_et_tables,
    detruit_database,
    get_connection_string,
    is_sql_server_running,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "DB_TEST")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_PORT = os.getenv("DB_PORT", 1433)
TRUST_SERVER_CERTIFICATE = (
    "yes" if os.getenv("TRUST_SERVER_CERTIFICATE", "no").lower() == "yes" else "no"
)


# docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Password123" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2025-latest
PYODBC_CONNECTION_STRING = get_connection_string(
    DB_DRIVER,
    os.getenv("DB_SERVER"),
    DB_PORT,
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    trust_server_certificate=TRUST_SERVER_CERTIFICATE == "yes",
    encrypt=False,
)


@pytest.fixture(scope="session", autouse=True)
def cree_database():
    # Crée la base avant tout test
    if not is_sql_server_running(PYODBC_CONNECTION_STRING):
        logger.critical("Impossible de trouver le serveur de base de données")
        pytest.exit(
            "SQL Server introuvable, le container est-il démarré ?", returncode=1
        )
    if not cree_database_et_tables(os.getenv("DB_NAME"), PYODBC_CONNECTION_STRING):
        logger.critical("Impossible de créer les tables.")
        pytest.exit("Impossible de créer les tables.", returncode=1)
    yield
    detruit_database(os.getenv("DB_NAME"), PYODBC_CONNECTION_STRING)


@pytest.fixture(scope="function")
def session(cree_database):
    engine = create_engine(
        f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{DB_PORT}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}&TrustServerCertificate={TRUST_SERVER_CERTIFICATE}",
        echo=True,
        future=True,
    )
    with Session(engine) as session:
        yield session
