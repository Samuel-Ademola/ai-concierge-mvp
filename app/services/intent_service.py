def detect_intent(message: str):
    text = message.lower()

    # FOOD / DINING
    if any(word in text for word in ["food", "restaurant", "eat", "dinner", "lunch", "breakfast"]):
        return "food_request"

    # TRANSPORT
    if any(word in text for word in ["taxi", "uber", "bolt", "transport", "ride", "car"]):
        return "transport_request"

    # BOOKING
    if any(word in text for word in ["book", "reservation", "reserve", "booking", "hotel room"]):
        return "booking_request"

    # HOTEL SERVICES
    if any(word in text for word in ["room service", "clean", "laundry", "towel", "housekeeping"]):
        return "hotel_service_request"

    # LOCAL INFO
    if any(word in text for word in ["near me", "around", "location", "close by"]):
        return "location_request"

    return "general_question"