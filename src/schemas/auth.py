from datetime import datetime

from pydantic import BaseModel



class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str

class RedirectResponse(BaseModel):
    redirect_url: str
    
class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

