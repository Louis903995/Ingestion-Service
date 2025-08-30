from fastapi import APIRouter
from app.models.numbers import NumbersResponse
from app.services.numbers import generate_numbers

router = APIRouter()

@router.get("/numbers", response_model=NumbersResponse)
async def get_numbers():
    return generate_numbers()
