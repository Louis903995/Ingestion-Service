from fastapi import FastAPI
from app.api.routers import ticket

# from app.db import create_db_and_tables  # Optionnel : création auto des tables

app = FastAPI()

# Inclure les routes de chaque module
app.include_router(ticket.router, tags=["Tickets"])
# app.include_router(routes_enseigne.router, prefix="/enseignes", tags=["Enseignes"])

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()  # optionnel, pour créer les tables au démarrage

# Si tu veux lancer avec : uvicorn app.main:app --reload
