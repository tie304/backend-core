from typing import Optional
from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenIngress(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None
