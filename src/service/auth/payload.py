from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import jwt
from src.models import User
from src.settings import settings


class PayloadService:
    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        """Verifies the validity of a refresh token and returns its payload."""
        try:
            payload = jwt.decode(
                token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def verify_access_token(token: str) -> dict:
        """Verifies the validity of an access token and returns its payload."""
        try:
            payload = jwt.decode(
                token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid access token")

    @classmethod
    def get_token_payload(cls, token: str, is_refresh: bool = False) -> dict:
        """Extracts and verifies payload from a token (access or refresh)."""
        token = token.replace("Bearer ", "")
        try:
            if is_refresh:
                return cls.verify_refresh_token(token)
            return cls.verify_access_token(token)
        except HTTPException:
            raise

    @classmethod
    def generate_tokens(cls, user: User) -> dict:
        """Генерация JWT токенов."""
        token_data = {"sub": user.yandex_id}

        tokens = {
            "access_token": cls._create_token(
                data=token_data,
                secret=settings.ACCESS_SECRET_KEY,
                expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
            "refresh_token": cls._create_token(
                data=token_data,
                secret=settings.REFRESH_SECRET_KEY,
                expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            ),
        }
        return tokens

    @staticmethod
    def _create_token(data: dict, secret: str, expires_minutes: int) -> str:
        expires = datetime.utcnow() + timedelta(minutes=expires_minutes)
        data.update({"exp": expires})
        token = jwt.encode(data, secret, algorithm=settings.ALGORITHM)
        return token
