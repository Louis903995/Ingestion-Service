import os


def load_env_file_to_environ():
    filename = ".env"
    if not os.path.exists(filename):
        return  # Ne fait rien si le fichier n'existe pas

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Ignore les lignes vides et commentaires
            if "=" not in line:
                continue  # Ignore les lignes invalides
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value


