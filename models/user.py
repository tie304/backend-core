import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy.sql import expression, func
from pydantic import BaseModel
from depends import metadata


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column(
        "disabled", sqlalchemy.Boolean, server_default=expression.false()
    ),
    sqlalchemy.Column(
        "verified", sqlalchemy.Boolean, server_default=expression.false()
    ),
    sqlalchemy.Column("created_on", sqlalchemy.DateTime, server_default=func.now()),
    sqlalchemy.Column("last_login", sqlalchemy.DateTime),
)


class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    disabled: bool = False
    verified: bool = False
    created_on: datetime.datetime  # postgres default
    last_login: Optional[datetime.datetime]


class UserSignup(BaseModel):
    email: str
    password: str


class UserOutput(User):
    hashed_password: str
