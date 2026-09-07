import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy import select

from app.database import SessionLocal
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.models.guest import Guest

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

password_hash = PasswordHash.recommended()
security = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        return password_hash.verify(password, stored_hash)
    except (TypeError, ValueError):
        return False


def create_access_token(user_id: int | str, role: str) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_user(
    name: str,
    email: str,
    password: str,
) -> User:
    db = SessionLocal()

    try:
        normalized_email = email.lower().strip()

        existing = db.execute(
            select(User).where(User.email == normalized_email)
        ).scalar_one_or_none()

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        user = User(
            name=name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
            role="guest",
            is_active=True,
        )

        db.add(user)
        db.flush()

        guest = Guest(
            user_id=str(user.id),
            user_pk=user.id,
            name=user.name,
            email=user.email,
            language="English",
            room_preference="Standard",
            requests="",
        )

        db.add(guest)
        db.commit()
        db.refresh(user)

        return user

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def authenticate_user(
    email: str,
    password: str,
) -> User | None:
    db = SessionLocal()

    try:
        normalized_email = email.lower().strip()

        user = db.execute(
            select(User).where(
                User.email == normalized_email,
                User.is_active.is_(True),
            )
        ).scalar_one_or_none()

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    finally:
        db.close()


def create_password_reset_token(
    email: str,
) -> str | None:
    db = SessionLocal()

    try:
        normalized_email = email.lower().strip()

        user = db.execute(
            select(User).where(
                User.email == normalized_email,
                User.is_active.is_(True),
            )
        ).scalar_one_or_none()

        if user is None:
            return None

        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()

        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=30)

        token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        db.add(token)
        db.commit()

        return raw_token

    finally:
        db.close()


def reset_password(
    token: str,
    new_password: str,
) -> bool:
    db = SessionLocal()

    try:
        token_hash = hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

        reset_token = db.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash,
            )
        ).scalar_one_or_none()

        if reset_token is None:
            return False

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if reset_token.used_at is not None:
            return False

        if reset_token.expires_at <= now:
            return False

        user = db.get(User, reset_token.user_id)

        if user is None or not user.is_active:
            return False

        user.password_hash = hash_password(new_password)
        reset_token.used_at = now

        db.commit()

        return True

    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, str]:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "require": [
                    "sub",
                    "role",
                    "iat",
                    "exp",
                ]
            },
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    return {
        "user_id": str(payload["sub"]),
        "role": str(payload["role"]),
    }


def get_current_user_record(
    current_user: dict[str, str] = Depends(get_current_user),
) -> User:
    db = SessionLocal()

    try:
        try:
            user_id = int(current_user["user_id"])
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user identity",
            )

        user = db.get(User, user_id)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is unavailable",
            )

        return user

    finally:
        db.close()


def require_staff(
    current_user: dict[str, str] = Depends(get_current_user),
) -> dict[str, str]:
    if current_user["role"] != "staff":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required",
        )

    return current_user
