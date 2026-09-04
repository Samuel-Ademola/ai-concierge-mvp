import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.guest import Guest
from app.models.guest_request import GuestRequest
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.stay import Stay
from app.models.user import User
from app.routes.chat import router as chat_router
from app.routes.settings import router as settings_router
from app.routes.requests import router as requests_router
from app.routes.auth import router as auth_router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Concierge")

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "name": "AI Concierge API",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


app.include_router(chat_router)
app.include_router(settings_router)
app.include_router(requests_router)
app.include_router(auth_router)
