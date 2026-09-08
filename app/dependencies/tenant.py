from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.tenant_service import get_user_hotel


def get_current_hotel(
    db: Session = Depends(get_db),
    current_user: dict[str, str] = Depends(get_current_user),
):
    return get_user_hotel(
        db=db,
        user_id=int(current_user["user_id"]),
    )