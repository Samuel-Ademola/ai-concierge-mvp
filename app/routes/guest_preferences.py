from fastapi import APIRouter

from app.schemas.guest_preferences_schema import (
    GuestPreferenceCreate,
    GuestPreferenceResponse
)


router = APIRouter(
    prefix="/guest-preferences",
    tags=["Guest Preferences"]
)


guest_preferences = []


@router.post("/", response_model=GuestPreferenceResponse)
def create_guest_preference(
    preference: GuestPreferenceCreate
):

    guest_id = len(guest_preferences) + 1

    guest = {
        "id": guest_id,
        **preference.model_dump()
    }

    guest_preferences.append(guest)

    return guest