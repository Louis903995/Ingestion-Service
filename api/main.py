from fastapi import FastAPI
from routes.client_routes import router as client_router
from routes.ticket_routes import router as ticket_router
from routes.categorie_routes import router as categorie_router
from routes.supermarche_routes import router as supermarche_router

app = FastAPI()

# Inclusion des routeurs
app.include_router(client_router)
app.include_router(ticket_router)
app.include_router(categorie_router)
app.include_router(supermarche_router)