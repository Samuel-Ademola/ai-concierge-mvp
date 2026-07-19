from fastapi import APIRouter, HTTPException

from app.schemas.guest_preferences_schema import (
    GuestPreferencesCreate,
    GuestPreferencesResponse,
)

router = APIRouter(
    prefix="/preferences",
    tags=["Guest Preferences"]
)

preferences_db = {}
current_id = 1


@router.post(
    "/",
    response_model=GuestPreferencesResponse,
    status_code=201
)
def create_preferences(
    preferences: GuestPreferencesCreate,
):
    global current_id

    record = {
        "id": current_id,
        **preferences.model_dump(),
    }

    preferences_db[current_id] = record
    current_id += 1

    return record


@router.get(
    "/{guest_id}",
    response_model=GuestPreferencesResponse,
)
def get_preferences(guest_id: int):
    preference = preferences_db.get(guest_id)

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="Guest preferences not found",
        )

    return preference