import logging
from sqlmodel import create_engine, Session

from app.config import (
    get_db_driver,
    get_db_name,
    get_db_password,
    get_db_port,
    get_db_server,
    get_db_user,
    get_trust_server_certificate,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

enseignes_dict = None
produit_categorie_dict = None


def construit_database_url():
    user = get_db_user()
    password = get_db_password()
    server = get_db_server()
    port = get_db_port()
    dbname = get_db_name()
    driver = get_db_driver()
    trust = get_trust_server_certificate()
    return (
        f"mssql+pyodbc://{user}:{password}@{server}:{port}/{dbname}"
        f"?driver={driver.replace(' ', '+')}&TrustServerCertificate={trust}"
    )


DATABASE_URL = construit_database_url()

# Création de l'engine SQLModel
engine = create_engine(DATABASE_URL, echo=False, future=True)


# Dependency à utiliser dans FastAPI (ou tes services)
def get_session():
    with Session(engine) as session:
        yield session
