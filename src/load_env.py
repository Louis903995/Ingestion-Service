import os


def load_env_file_to_environ():
    filename = ".env"
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value
