https://learn.microsoft.com/fr-fr/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver17&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#tabpanel_1_ubuntu18-install


<!-- sudo apt update
sudo apt install -y curl gnupg
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/microsoft.gpg >/dev/null
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/ubuntu/22.04/mssql-server-2025 focal main" | sudo tee /etc/apt/sources.list.d/mssql-server.list
sudo apt update


# Ajouter le dépôt Microsoft
sudo add-apt-repository "$(curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list)"
sudo apt-get update -->

# Installer le pilote ODBC
sudo apt-get install -y msodbcsql18



# installation local d'une container SQL Server (pour le dev)
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=MotDePasseUltraFort123!" \
   -p 1433:1433 --name sqlserver-dev -d mcr.microsoft.com/mssql/server:2022-latest