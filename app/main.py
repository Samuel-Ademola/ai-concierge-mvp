from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.guest_preferences import router as guest_preferences_router


app = FastAPI(title="AI Concierge MVP")


@app.get("/")
def home():
    return {
        "status": "AI Concierge MVP running"
    }


app.include_router(chat_router)
app.include_router(guest_preferences_router)