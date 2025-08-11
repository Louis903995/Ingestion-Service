from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional
import datetime

app = FastAPI()

# 1. Définir les modèles avec SQLModel 

class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    budget: float
    date_enregistrement: datetime.datetime

class Ticket(SQLModel, table=True):
    id_ticket: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.client_id")
    libelle: str

# 2. Connexion à ta base Azure SQL

server = "simplon-certif.database.windows.net"
database = "simplon-certif"
username = "sqladminuser"
password = "LouisMoises123"
driver = "ODBC Driver 18 for SQL Server"

DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver.replace(' ', '+')}"

engine = create_engine(DATABASE_URL, echo=True)

# 3. Dépendance pour avoir une session DB

def get_session():
    with Session(engine) as session:
        yield session

# 5. Routes FastAPI

@app.get("/clients", response_model=List[Client])
def read_clients(session: Session = Depends(get_session)):
    clients = session.exec(select(Client)).all()
    return clients

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@app.post("/clients", response_model=Client)
def create_client(client: Client, session: Session = Depends(get_session)):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client
