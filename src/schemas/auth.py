from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class RedirectResponse(BaseModel):
    redirect_url: str
