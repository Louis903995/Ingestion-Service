from datetime import datetime
from random import randint
from app.schemas.allures import AlluresResponse, MesureTemporelle

def generate_allures() -> AlluresResponse:
    depense_constate = [MesureTemporelle (d=datetime(2025, 9, 1, 0, 0), v = 80), 
                        MesureTemporelle (d=datetime(2025, 8, 25, 0, 0), v = 90),
                        MesureTemporelle (d=datetime(2025, 8, 18, 0, 0), v = 100)]
    depense_predite = [MesureTemporelle (d=datetime(2025, 9, 8, 0, 0), v = 120)]
    return AlluresResponse(depense_constate = depense_constate, depense_predite = depense_predite)
