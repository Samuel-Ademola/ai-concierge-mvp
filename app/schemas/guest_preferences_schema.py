from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Language(str, Enum):
    english = "English"
    french = "French"
    spanish = "Spanish"


class RoomPreference(str, Enum):
    standard = "Standard"
    deluxe = "Deluxe"
    suite = "Suite"


class GuestPreferencesCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    language: Language
    room_preference: RoomPreference
    requests: Optional[str] = Field(
        default="",
        max_length=500
    )


class GuestPreferencesResponse(GuestPreferencesCreate):
    id: int