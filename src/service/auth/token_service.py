from fastapi import Response
from src.settings import settings
from src.service.auth.payload import PayloadService
from src.models.user import User


class TokenService:
    """Service for managing authentication tokens.

    This service handles the generation and setting of authentication tokens
    in HTTP cookies.

    Attributes:
        payload_service (PayloadService): Service for handling token payloads
    """

    def __init__(self, payload_service: PayloadService):
        """Initialize TokenService with payload service.

        Args:
            payload_service (PayloadService): Service for handling token payloads
        """
        self.payload_service = payload_service

    def set_auth_cookies(self, response: Response, tokens: dict) -> None:
        """Set authentication tokens in HTTP cookies.

        Sets both access and refresh tokens as HTTP-only cookies with appropriate
        expiration times and security settings.

        Args:
            response (Response): FastAPI response object
            tokens (dict): Dictionary containing access and refresh tokens
        """
        response.set_cookie(
            key="access_token",
            value=f"Bearer {tokens['access_token']}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {tokens['refresh_token']}",
            httponly=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

    def generate_and_set_tokens(self, response: Response, user: User) -> dict:
        """Generate tokens and set them in cookies.

        This method combines token generation and cookie setting into a single operation.

        Args:
            response (Response): FastAPI response object
            user (User): The user to generate tokens for

        Returns:
            dict: Generated authentication tokens
        """
        tokens = self.payload_service.generate_tokens(user)
        self.set_auth_cookies(response, tokens)
        return tokens
