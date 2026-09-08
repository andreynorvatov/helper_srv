from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)