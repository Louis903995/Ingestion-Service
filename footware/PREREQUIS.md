git
python >= 3.12
pdm
az cli
Docker
Make
odbc + driver mssql version 18

plugin vscode MSSQL (optionel)

(pdm lock si pdm.lock existe déjà)
pdm install -G :all


docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Password123" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2025-latest