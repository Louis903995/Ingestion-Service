FROM python:3.12

# Installer curl, gnupg2, et ajouter le repo Microsoft
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /usr/share/keyrings/microsoft.gpg >/dev/null \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" | tee /etc/apt/sources.list.d/mssql-release.list

# Installer le driver ODBC SQL Server
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Créer le dossier app dans l'image
RUN mkdir /app

# Copier requirements.txt et installer les packages Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["tail", "-f", "/dev/null"]
