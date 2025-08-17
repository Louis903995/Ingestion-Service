from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete
from typing import List, Optional
import datetime

app = FastAPI()

# 1. Définir les Classes 

# Modèle Client principal (table SQL)
class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    budget: float
    date_enregistrement: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Modèle pour mise à jour 
class ClientUpdate(SQLModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    budget: Optional[float] = None

# Créer un client en ne specifiant que le nom, prenom et le budget 
class ClientCreate(SQLModel):
    nom: str
    prenom: str
    budget: float

class Ticket(SQLModel, table=True):
    id_ticket: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.client_id")
    libelle: str

class Categorie(SQLModel, table=True):
    id_cat: Optional[int] = Field(default=None, primary_key=True)
    id_ticket: int = Field(foreign_key="ticket.id_ticket")
    libelle: str
    categorie: str

class Supermarche(SQLModel, table=True):
    id_supermarche: Optional[int] = Field(default=None, primary_key=True)
    id_ticket: int = Field(foreign_key="ticket.id_ticket")
    nom_magasin: str
    date_achat: datetime.date
    prix_total: float


# 2. Connexion à la base Azure SQL

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

# 4. Routes FastAPI concernant les Clients

@app.get("/clients", response_model=List[Client])
def read_clients(session: Session = Depends(get_session)):
    return session.exec(select(Client)).all()

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@app.post("/clients", response_model=Client)
def create_client(client_create: ClientCreate, session: Session = Depends(get_session)):
    client = Client.from_orm(client_create)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client_update: ClientUpdate, session: Session = Depends(get_session)):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    update_data = client_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}") # on peut supprimer un client sans que cela n'ai d'effets sur les tickets enregistrés 
def delete_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    session.delete(client)
    session.commit()
    return {"message": "Client supprimé avec succès"}


# 5. Routes FastAPI concernant les tickets

# Lire tous les tickets
@app.get("/tickets", response_model=List[Ticket])
def read_tickets(session: Session = Depends(get_session)):
    tickets = session.exec(select(Ticket)).all()
    return tickets

# Lire un ticket par son ID
@app.get("/tickets/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    return ticket

# Créer un ticket
@app.post("/tickets", response_model=Ticket)
def create_ticket(ticket: Ticket, session: Session = Depends(get_session)):
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

# Modifier un ticket
@app.put("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket_update: Ticket, session: Session = Depends(get_session)):
    db_ticket = session.get(Ticket, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")

    for key, value in ticket_update.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

# Supprimer un ticket
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, session: Session = Depends(get_session)):
    db_ticket = session.get(Ticket, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")

    session.delete(db_ticket)
    session.commit()
    return {"message": "Ticket supprimé avec succès"}



# 6. Routes FastAPI concernant les catégories 
# Lire toutes les catégories
@app.get("/categories", response_model=List[Categorie])
def read_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Categorie)).all()
    return categories

# Lire une catégorie par son ID
@app.get("/categories/{categorie_id}", response_model=Categorie)
def read_category(categorie_id: int, session: Session = Depends(get_session)):
    category = session.get(Categorie, categorie_id)
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return category

# Créer une catégorie
@app.post("/categories", response_model=Categorie)
def create_category(category: Categorie, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Modifier une catégorie
@app.put("/categories/{categorie_id}", response_model=Categorie)
def update_category(categorie_id: int, category_update: Categorie, session: Session = Depends(get_session)):
    db_category = session.get(Categorie, categorie_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    for key, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

# Supprimer une catégorie
@app.delete("/categories/{categorie_id}")
def delete_category(categorie_id: int, session: Session = Depends(get_session)):
    db_category = session.get(Categorie, categorie_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    session.delete(db_category)
    session.commit()
    return {"message": "Catégorie supprimée avec succès"}


# 7. Routes FastAPI concernant les supermarchés

# Lire tous les supermarchés
@app.get("/supermarches", response_model=List[Supermarche])
def read_supermarches(session: Session = Depends(get_session)):
    supermarches = session.exec(select(Supermarche)).all()
    return supermarches

# Lire un supermarché par son ID
@app.get("/supermarches/{supermarche_id}", response_model=Supermarche)
def read_supermarche(supermarche_id: int, session: Session = Depends(get_session)):
    supermarche = session.get(Supermarche, supermarche_id)
    if not supermarche:
        raise HTTPException(status_code=404, detail="Supermarché non trouvé")
    return supermarche

# Créer un supermarché
@app.post("/supermarches", response_model=Supermarche)
def create_supermarche(supermarche: Supermarche, session: Session = Depends(get_session)):
    session.add(supermarche)
    session.commit()
    session.refresh(supermarche)
    return supermarche

# Modifier un supermarché
@app.put("/supermarches/{supermarche_id}", response_model=Supermarche)
def update_supermarche(supermarche_id: int, supermarche_update: Supermarche, session: Session = Depends(get_session)):
    db_supermarche = session.get(Supermarche, supermarche_id)
    if not db_supermarche:
        raise HTTPException(status_code=404, detail="Supermarché non trouvé")

    for key, value in supermarche_update.dict(exclude_unset=True).items():
        setattr(db_supermarche, key, value)

    session.add(db_supermarche)
    session.commit()
    session.refresh(db_supermarche)
    return db_supermarche

# Supprimer un supermarché
@app.delete("/supermarches/{supermarche_id}")
def delete_supermarche(supermarche_id: int, session: Session = Depends(get_session)):
    db_supermarche = session.get(Supermarche, supermarche_id)
    if not db_supermarche:
        raise HTTPException(status_code=404, detail="Supermarché non trouvé")

    session.delete(db_supermarche)
    session.commit()
    return {"message": "Supermarché supprimé avec succès"}
