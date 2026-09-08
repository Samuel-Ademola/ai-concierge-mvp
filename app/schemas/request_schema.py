from datetime import datetime

from pydantic import BaseModel, field_validator


ALLOWED_STATUSES = {
    "pending",
    "confirmed",
    "completed",
    "cancelled",
}


class GuestRequestCreate(BaseModel):
    request_type: str
    details: str


class GuestRequestResponse(BaseModel):
    id: int
    request_id: str
    user_id: str
    request_type: str
    details: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class GuestRequestStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.lower().strip()

        if value not in ALLOWED_STATUSES:
            raise ValueError(
                "Status must be pending, confirmed, completed, or cancelled"
            )

        return value
