from fastapi import APIRouter, Depends, HTTPException

from app.schemas.request_schema import (
    GuestRequestCreate,
    GuestRequestResponse,
    GuestRequestStatusUpdate,
)
from app.services.auth_service import get_current_user, require_staff
from app.services.request_service import (
    create_guest_request,
    get_guest_requests,
    update_guest_request_status,
)

router = APIRouter(
    prefix="/requests",
    tags=["requests"],
)


@router.post(
    "",
    response_model=GuestRequestResponse,
)
async def create_request(
    request: GuestRequestCreate,
    current_user: dict[str, str] = Depends(get_current_user),
):
    return create_guest_request(
        user_id=current_user["user_id"],
        request_type=request.request_type,
        details=request.details,
    )


@router.get(
    "",
    response_model=list[GuestRequestResponse],
)
async def get_requests(
    current_user: dict[str, str] = Depends(get_current_user),
):
    return get_guest_requests(current_user["user_id"])


@router.patch(
    "/{request_id}",
    response_model=GuestRequestResponse,
)
async def update_request_status(
    request_id: str,
    update: GuestRequestStatusUpdate,
    current_user: dict[str, str] = Depends(require_staff),
):
    request = update_guest_request_status(
        request_id=request_id,
        status=update.status,
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Guest request not found",
        )

    return request