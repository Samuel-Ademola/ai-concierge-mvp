from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest
from app.services.intent_service import detect_intent
from app.services.response_service import generate_response

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    message = request.message
    user_id = request.user_id

    intent = detect_intent(message)

    response = generate_response(intent, user_id, message)

    return {
        "user_id": user_id,
        "message": message,
        "intent": intent,
        "response": response
    }