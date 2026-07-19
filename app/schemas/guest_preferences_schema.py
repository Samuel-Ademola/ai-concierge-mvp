from pydantic import BaseModel, EmailStr, Field


class GuestPreferenceCreate(BaseModel):
    guest_name: str
    email: EmailStr
    language: str
    room_preference: str
    requests: str = Field(max_length=500)


class GuestPreferenceResponse(GuestPreferenceCreate):
    id: int