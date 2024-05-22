from fastapi import APIRouter

from app.api.routes import cards

api_router = APIRouter()
api_router.include_router(cards.router, prefix="/cards", tags=["cards"])

