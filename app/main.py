from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import Session
from app.routers import clients, ticket
from app.services.enseigne_service import EnseigneService
from app.db.database import engine
import app.db.database as db
from app.services.produit_categorie_service import ProduitCategorieService
from app.routers.times import data_router

load_dotenv(dotenv_path=".env", override=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        db.enseignes_dict = EnseigneService.get_enseignes_dict(session)
        db.produit_categorie_dict = ProduitCategorieService.get_produit_categorie_dict(
            session
        )
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ticket.router, tags=["Tickets"])
app.include_router(clients.router, tags=["Clients"])
app.include_router(data_router)
