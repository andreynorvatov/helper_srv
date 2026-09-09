from fastapi import APIRouter

from config import settings
from src.openrouter.routes import openrouter_router
from src.currency.routes import currency_router

api_router = APIRouter()

api_router.include_router(openrouter_router, prefix=f"{settings.API_V1_STR}/openrouter", tags=["AIP Openrouter"])
api_router.include_router(currency_router, prefix=f"{settings.API_V1_STR}/currency", tags=["AIP Currency"])