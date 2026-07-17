from app.services.memory_service import get_memory, update_memory


def generate_response(intent: str, user_id: str, message: str):

    memory = get_memory(user_id)

    # store last intent
    update_memory(user_id, "last_intent", intent)
    update_memory(user_id, "last_message", message)

    # context-aware responses
    if intent == "food_request":
        if memory.get("last_intent") == "food_request":
            return "Would you like me to narrow it down to nearby restaurants or cuisine type?"

        return "Sure, are you looking for local food or fine dining?"

    if intent == "transport_request":
        return "Do you need a ride now or scheduled pickup?"

    if intent == "booking_request":
        return "What date and type of room would you like to book?"

    if intent == "hotel_service_request":
        return "What hotel service do you need help with?"

    if intent == "location_request":
        return "What kind of places are you looking for nearby?"

    return "Can you give me a bit more detail so I can help you better?"