from dotenv import load_dotenv

from app.config import (
    get_db_driver,
    get_db_name,
    get_db_password,
    get_db_port,
    get_db_server,
    get_db_user,
    get_trust_server_certificate,
)

load_dotenv()  # exceptionnel pour charger .env avant toutes autre opération

import pytest  # noqa: E402
import logging  # noqa: E402


from sqlmodel import Session, create_engine  # noqa: E402
from app.db.database import engine  # noqa: E402

from app.services.enseigne_service import EnseigneService  # noqa: E402
from tests.pyodbc_utils import (  # noqa: E402
    cree_database_et_tables,
    detruit_database,
    execute_script_sql,
    get_connection_string,
    is_sql_server_running,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=MotDePasseUltraFort123!" \
# -p 1433:1433 --name sqlserver-dev -d mcr.microsoft.com/mssql/server:2025-latest
PYODBC_CONNECTION_STRING = get_connection_string(
    get_db_driver(),
    get_db_server(),
    get_db_port(),
    get_db_user(),
    get_db_password(),
    trust_server_certificate=get_trust_server_certificate(),
    encrypt=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    execute_script_sql(
        "tests/database/sql/ajoute_categories.sql",
        get_db_name(),
        PYODBC_CONNECTION_STRING,
    )
    execute_script_sql(
        "tests/database/sql/ajoute_enseignes.sql",
        get_db_name(),
        PYODBC_CONNECTION_STRING,
    )
    yield


# lit les val. d'Enseigne et les colle dans enseigne_dict au startup
@pytest.fixture(autouse=True)
def update_enseignes_dict():
    import app.db.database

    with Session(engine) as session:
        app.db.database.enseignes_dict = EnseigneService.get_enseignes_dict(session)
    yield


@pytest.fixture(scope="session", autouse=True)
def cree_database():
    # Crée la base avant tout test
    if not is_sql_server_running(PYODBC_CONNECTION_STRING):
        logger.critical("Impossible de trouver le serveur de base de données")
        pytest.exit(
            "SQL Server introuvable, le container est-il démarré ?", returncode=1
        )
    if not cree_database_et_tables(get_db_name(), PYODBC_CONNECTION_STRING):
        logger.critical("Impossible de créer les tables.")
        pytest.exit("Impossible de créer les tables.", returncode=1)
    yield
    detruit_database(get_db_name(), PYODBC_CONNECTION_STRING)


@pytest.fixture(scope="function")
def session(cree_database):
    engine = create_engine(
        f"mssql+pyodbc://{get_db_user()}:{get_db_password()}"
        f"@{get_db_server()}:{get_db_port()}/{get_db_name()}"
        f"?driver={get_db_driver().replace(' ', '+')}"
        f"&TrustServerCertificate={get_trust_server_certificate()}",
        echo=True,
        future=True,
    )
    with Session(engine) as session:
        yield session
