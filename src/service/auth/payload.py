from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import jwt
from src.models import User
from src.settings import settings


class PayloadService:
    """Service for handling JWT token payload operations.

    This service provides methods for verifying, generating, and managing
    JWT token payloads for both access and refresh tokens.

    Methods:
        verify_refresh_token: Verify refresh token validity
        verify_access_token: Verify access token validity
        get_token_payload: Extract and verify token payload
        generate_tokens: Generate new JWT tokens
        _create_token: Create a single JWT token
    """

    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        """Verify the validity of a refresh token and return its payload.

        Args:
            token (str): The refresh token to verify

        Returns:
            dict: The decoded token payload

        Raises:
            HTTPException: 401 if token is invalid
        """
        try:
            payload = jwt.decode(
                token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def verify_access_token(token: str) -> dict:
        """Verify the validity of an access token and return its payload.

        Args:
            token (str): The access token to verify

        Returns:
            dict: The decoded token payload

        Raises:
            HTTPException: 401 if token is invalid
        """
        try:
            payload = jwt.decode(
                token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid access token")

    @classmethod
    def get_token_payload(cls, token: str, is_refresh: bool = False) -> dict:
        """Extract and verify payload from a token (access or refresh).

        Args:
            token (str): The token to process
            is_refresh (bool, optional): Whether the token is a refresh token.
                Defaults to False.

        Returns:
            dict: The decoded token payload

        Raises:
            HTTPException: 401 if token is invalid
        """
        token = token.replace("Bearer ", "")
        try:
            if is_refresh:
                return cls.verify_refresh_token(token)
            return cls.verify_access_token(token)
        except HTTPException:
            raise

    @classmethod
    def generate_tokens(cls, user: User) -> dict:
        """Generate JWT tokens for a user.

        Creates both access and refresh tokens with appropriate expiration times.

        Args:
            user (User): The user to generate tokens for

        Returns:
            dict: Dictionary containing access and refresh tokens
        """
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
        """Create a JWT token with the given parameters.

        Args:
            data (dict): The payload data to encode
            secret (str): The secret key to sign the token
            expires_minutes (int): Number of minutes until token expiration

        Returns:
            str: The generated JWT token
        """
        expires = datetime.utcnow() + timedelta(minutes=expires_minutes)
        data.update({"exp": expires})
        token = jwt.encode(data, secret, algorithm=settings.ALGORITHM)
        return token
