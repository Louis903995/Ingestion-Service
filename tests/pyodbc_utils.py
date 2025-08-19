import logging
import pyodbc
import re
import socket


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRIPT_CREATION_TOUTES_TABLES = "tests/database/sql/create_toutes_tables.sql"


def get_connection_string(
    driver: str,
    server: str,
    port: int,
    username: str,
    password: str,
    trust_server_certificate: bool = False,
    encrypt: bool = True,
    connection_timeout: int = 5,
) -> str:
    return (
        f"DRIVER={{{driver}}};SERVER={server},{port};UID={username};PWD={password};"
        f"TrustServerCertificate={'yes' if trust_server_certificate else 'no'};"
        f"Encrypt={'yes' if encrypt else 'no'};"
        f"Connection Timeout={connection_timeout};"
    )


def is_sql_server_running(connection_string: str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            host, port = (
                re.search(r"SERVER=([^;]*)", connection_string).group(1).split(",")
            )
            port = int(port)
            timeout = int(
                re.search(r"Connection Timeout=([^;]*)", connection_string).group(1)
            )
            sock.settimeout(timeout)
            sock.connect((host, port))
            with pyodbc.connect(connection_string):
                return True
    except Exception as e:
        logger.critical(f"Erreur : {e}")
        return False


def force_db_dans_conn_string(connection_string: str, db_name) -> str:
    if "DATABASE=" in connection_string:
        return re.sub(r"(DATABASE=)[^;]+", f"DATABASE={db_name}", connection_string)
    else:
        separator = ";" if not connection_string.endswith(";") else ""
        return f"{connection_string}{separator}DATABASE={db_name};"


def execute_script_sql(script_path: str, db_name: str, connection_string: str) -> bool:
    try:
        with pyodbc.connect(
            force_db_dans_conn_string(connection_string, db_name)
        ) as db_conn:
            with open(script_path, "r", encoding="utf-8") as file:
                db_cursor = db_conn.cursor()
                sql_script = file.read()
                for batch in sql_script.split("GO"):
                    batch = batch.strip()
                    if batch:
                        db_cursor.execute(batch)
                db_conn.commit()
                return True
    except pyodbc.Error as e:
        logger.critical(f"Erreur : {e}")
        return False


def cree_database_et_tables(db_name: str, connection_string: str) -> bool:
    try:
        master_connection_string = force_db_dans_conn_string(
            connection_string, "master"
        )
        db_existe = False
        with pyodbc.connect(master_connection_string, autocommit=True) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sys.databases WHERE name = ?", db_name)
            if cursor.fetchone():
                db_existe = True

        if not db_existe:
            # Connexion séparée, rien que pour CREATE DATABASE sinon ça plante avec pyodbc 18
            # (merci copilot!!)
            with pyodbc.connect(master_connection_string, autocommit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"CREATE DATABASE [{db_name}]"
                )  # Toujours utiliser les crochets !
                print(f"Base {db_name} créée.")

        return execute_script_sql(
            SCRIPT_CREATION_TOUTES_TABLES, db_name, connection_string
        )

    except pyodbc.Error as e:
        logger.critical(f"Erreur : {e}")
        return False


def detruit_database(db_name: str, connection_string: str) -> bool:
    master_connection_string = force_db_dans_conn_string(connection_string, "master")
    try:
        with pyodbc.connect(master_connection_string, autocommit=True) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM sys.databases WHERE name = '{db_name}'")
            if cursor.fetchone():
                # Ferme les connexions actives à la base (évite les erreurs)
                cursor.execute(
                    f"""
                    ALTER DATABASE {db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                    DROP DATABASE {db_name};
                """
                )
        return True
    except pyodbc.Error as e:
        logger.critical(f"Erreur : {e}")
        return False
