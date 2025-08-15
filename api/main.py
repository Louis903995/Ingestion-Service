from fastapi import FastAPI
from .routes.client_routes import router as client_router

app = FastAPI()

# Inclusion des routeurs
app.include_router(client_router)
