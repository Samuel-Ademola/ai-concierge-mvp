from fastapi import FastAPI

from app.routes.chat import router as chat_router

app = FastAPI(title="AI Concierge MVP")


@app.get("/")
def home():
    return {
        "status": "AI Concierge MVP running"
    }


app.include_router(chat_router)