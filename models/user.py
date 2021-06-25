import datetime
from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    email: str
    hashed_password: str
    disabled: bool = False
    verified: bool = False
    created_on: datetime.datetime # postgres default
    last_login: Optional[datetime.datetime]


class UserSignup(BaseModel):
    email: str
    password: str


class UserOutput(User):
    hashed_password: str


