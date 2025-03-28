from pydantic import BaseModel


class AuthResponse(BaseModel):
    """Authentication response model.

    This model represents the authentication tokens returned after successful login.

    Attributes:
        access_token (str): JWT access token for API authentication
        refresh_token (str): JWT refresh token for obtaining new access tokens
    """

    access_token: str
    refresh_token: str


class RedirectResponse(BaseModel):
    """OAuth redirect response model.

    This model represents the redirect URL for OAuth authentication flow.

    Attributes:
        redirect_url (str): URL to redirect the user to for OAuth authentication
    """

    redirect_url: str
