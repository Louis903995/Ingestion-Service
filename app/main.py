# Standard Library
from contextlib import asynccontextmanager

# Third-party Libraries
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import Session

# Application Modules
from app.db.database import engine
import app.db.database as db
from app.routers import allures, clients, ticket
from app.services.enseigne_service import EnseigneService
from app.services.produit_categorie_service import ProduitCategorieService


# Load environment variables
load_dotenv(dotenv_path=".env", override=False)


# Lifespan context for initializing app resources
@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        db.enseignes_dict = EnseigneService.get_enseignes_dict(session)
        db.produit_categorie_dict = ProduitCategorieService.get_produit_categorie_dict(session)
    yield


# FastAPI application instance
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(ticket.router, tags=["Tickets"])
app.include_router(clients.router, tags=["Clients"])
app.include_router(allures.router, tags=["Allures"])