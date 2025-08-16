import pyodbc

SCRIPT_CREATION_TOUTES_TABLES = "sql/create_toutes_tables.sql"


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
        f"TrustServerCertificate={"yes" if trust_server_certificate else "no"};"
        f'Encrypt={"yes" if encrypt else "no" };'
        f"Connection Timeout={connection_timeout};"
    )


def is_sql_server_running(connection_string: str) -> bool:
    try:
        with pyodbc.connect(connection_string) as conn:
            return True
    except Exception as e:
        return False


def cree_database_et_tables(db_name: str, connection_string: str) -> bool:
    try:
        # si la connection string comporte le nom de la DB, on remplace par 'master'
        master_connection_string = connection_string.replace(
            "DATABASE={db_name}", "DATABASE=master"
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

        if "DATABASE=" in connection_string:
            db_connection_string = connection_string.replace(
                "DATABASE={db_name}", f"DATABASE={db_name}"
            )
        else:
            db_connection_string = f"{connection_string}DATABASE={db_name};"
        with pyodbc.connect(db_connection_string) as db_conn:
            with open(SCRIPT_CREATION_TOUTES_TABLES, "r", encoding="utf-8") as file:
                db_cursor = db_conn.cursor()
                sql_script = file.read()
                for batch in sql_script.split("GO"):
                    batch = batch.strip()
                    if batch:
                        db_cursor.execute(batch)

                db_conn.commit()
                return True

    except pyodbc.Error as e:
        print(f"Erreur : {e}")
        return False
