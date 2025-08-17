import pytest
import logging

from sqlmodel import Session, create_engine

from tests.pyodbc_utils import (
    cree_database_et_tables,
    detruit_database,
    get_connection_string,
    is_sql_server_running,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SERVER = "localhost"
PORT = 1433
USERNAME = "SA"
PASSWORD = "Password123"
DRIVER = "ODBC Driver 18 for SQL Server"
DB_NAME_TEST = "DB_TEST"


# docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Password123" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2025-latest
PYODBC_CONNECTION_STRING = get_connection_string(
    DRIVER,
    SERVER,
    PORT,
    USERNAME,
    PASSWORD,
    trust_server_certificate=True,
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
    if not cree_database_et_tables(DB_NAME_TEST, PYODBC_CONNECTION_STRING):
        logger.critical("Impossible de créer les tables.")
        pytest.exit("Impossible de créer les tables.", returncode=1)
    yield
    detruit_database(DB_NAME_TEST, PYODBC_CONNECTION_STRING)


@pytest.fixture(scope="function")
def session(cree_database):
    engine = create_engine(
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME_TEST}?driver={DRIVER.replace(' ', '+')}&TrustServerCertificate=yes",
        echo=True,
        future=True,
    )
    with Session(engine) as session:
        yield session
