import os


def get_app_insights_conn_string() -> str:
    return os.environ["APP_INSIGHT_CONNECTION_STRING"]


def get_db_user() -> str:
    return os.environ["DB_USER"]


def get_db_password() -> str:
    return os.environ["DB_PASSWORD"]


def get_db_server() -> str:
    return os.environ["DB_SERVER"]


def get_db_name() -> str:
    return os.environ["DB_NAME"]


def get_db_port() -> int:
    return int(os.environ.get("DB_PORT", "1433"))


def get_db_driver() -> str:
    return os.environ.get("DB_DRIVER", "ODBC Driver 18 for SQL Server")


def get_trust_server_certificate() -> str:
    return (
        "yes"
        if os.environ.get("TRUST_SERVER_CERTIFICATE", "no").lower() == "yes"
        else "no"
    )
