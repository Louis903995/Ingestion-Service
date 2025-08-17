from fastapi import FastAPI
from .routers.clients import router as client_router

app = FastAPI()

# Inclusion des routeurs
app.include_router(client_router)
