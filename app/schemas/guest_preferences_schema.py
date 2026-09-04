from pydantic import BaseModel, EmailStr


class GuestPreferenceBase(BaseModel):
    name: str
    email: EmailStr
    language: str
    roomPreference: str
    requests: str = ""


class GuestPreferenceCreate(GuestPreferenceBase):
    pass


class GuestPreferenceResponse(GuestPreferenceBase):
    id: int
