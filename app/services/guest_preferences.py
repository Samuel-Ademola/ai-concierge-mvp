from app.schemas.guest_preferences_schema import (
    GuestPreferenceResponse,
    GuestPreferenceCreate,
)


guest_preferences_db = {}

current_id = 1


def create_guest_preferences(
    preferences: GuestPreferenceCreate
):
    global current_id

    guest_preferences = GuestPreferenceResponse(
        id=current_id,
        **preferences.model_dump()
    )

    guest_preferences_db[current_id] = guest_preferences

    current_id += 1

    return guest_preferences


def get_guest_preferences(preference_id: int):
    return guest_preferences_db.get(preference_id)