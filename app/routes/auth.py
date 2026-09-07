from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    ResetPasswordRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_password_reset_token,
    create_user,
    get_current_user,
    get_current_user_record,
    reset_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(request: SignupRequest):
    user = create_user(
        name=request.name,
        email=request.email,
        password=request.password,
    )

    token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
        role=user.role,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(request: LoginRequest):
    user = authenticate_user(
        email=request.email,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
        role=user.role,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: dict[str, str] = Depends(get_current_user),
):
    user = get_current_user_record(current_user)

    return UserResponse(
        user_id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role,
    )


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
async def forgot_password(request: ForgotPasswordRequest):
    token = create_password_reset_token(request.email)

    # Development/MVP behavior:
    # return the token so the complete reset flow can be tested
    # without an email provider.
    if token is not None:
        return ForgotPasswordResponse(
            message=f"Password reset token: {token}",
        )

    # Do not reveal whether an email exists.
    return ForgotPasswordResponse(
        message="If an account exists for that email, a password reset link has been requested.",
    )


@router.post(
    "/reset-password",
    response_model=ForgotPasswordResponse,
)
async def reset_password_route(request: ResetPasswordRequest):
    success = reset_password(
        token=request.token,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token",
        )

    return ForgotPasswordResponse(
        message="Password has been reset successfully.",
    )
