from pydantic import BaseModel, EmailStr, Field


class SettingsForm(BaseModel):
    hotel_name: str = Field(..., min_length=1)
    contact_email: EmailStr
    timezone: str = "UTC"
