import os
from datetime import timedelta, datetime
from functools import wraps
import asyncio

from jose import jwt
from fastapi import HTTPException, status


def pack_invitation_code(storage_size: int) -> str:
    """Generate a invitation code with assigned storage size for new signed users."""
    pass


def unpack_invitation_code(invitation_code: str) -> int:
    """Get assigned storage size from invitation code."""
    pass


class Authentication:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def create_access_token(user_id: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        expires_delta = timedelta(minutes=expires_minutes)
        now = datetime.utcnow()
        expire = now + expires_delta
        to_encode = {"exp": expire, "iat": now.timestamp(), "userId": user_id}
        encoded_jwt = jwt.encode(to_encode, Authentication.JWT_SECRET_KEY, algorithm=Authentication.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _refresh_token(old_token: str) -> str:
        # Refresh token no more frequent than every 15 minutes
        payload = jwt.decode(old_token, Authentication.JWT_SECRET_KEY, algorithms=[Authentication.JWT_ALGORITHM])
        user_id: str = payload["userId"]
        issued_at: int = int(payload["iat"])
        if datetime.utcnow().timestamp() - issued_at >= 900:
            return Authentication.create_access_token(user_id)
        return old_token  # no need to refresh

    @staticmethod
    def get_authed_user_id_and_token(token: str) -> tuple[str, str]:
        unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, Authentication.JWT_SECRET_KEY, algorithms=[Authentication.JWT_ALGORITHM])
            user_id = payload["userId"]
            expire = int(payload["exp"])
        except Exception as e:
            unauthorized_exception.detail += f"{e}"
            raise unauthorized_exception
        if datetime.utcnow().timestamp() - expire < 0:  # Token has not expired
            return user_id, token

    @staticmethod
    def refresh_token_in_cookie(api_func):
        @wraps(api_func)
        async def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(api_func):
                response = await api_func(*args, **kwargs)
            else:
                response = api_func(*args, **kwargs)
            kwargs["response"].set_cookie(
                "token",
                Authentication._refresh_token(kwargs["user_id_token_tuple"][1]),
                Authentication.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                httponly=True,
            )
            return response

        return wrapper
