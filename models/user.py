import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import expression, func
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel
from depends import Base


class ApplicationRole(str, Enum):
    """
    Roles of the applicaton.

    ADMIN:
        Admin has access to all config and user admin routes
    USER:
        user has access to all the normal application routes
    """

    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, server_default=ApplicationRole.USER.value)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, server_default=expression.false())
    verified = Column(Boolean, server_default=expression.false())
    created_on = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)


class UserVerifed(Base):
    __tablename__ = "user_verification_map"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    code = Column(String)


class UserPasswordReset(Base):
    __tablename__ = "user_password_reset"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, unique=True)
    code = Column(String)


PydanticUser = sqlalchemy_to_pydantic(User)
PydanticUserVerified = sqlalchemy_to_pydantic(UserVerifed)
PydanticUserPasswordReset = sqlalchemy_to_pydantic(UserPasswordReset)

class UserBase(BaseModel):
    id: int
    email: str
    role: ApplicationRole
    hashed_password: str
    disabled: bool = False
    verified: bool = False
    created_on: datetime.datetime  # postgres default
    last_login: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class UserOutput(BaseModel):
    id: int
    email: str
    role: ApplicationRole
    disabled: bool = False
    verified: bool = False
    created_on: datetime.datetime  # postgres default
    last_login: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class UserSignup(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserPasswordIngress(BaseModel):
    password: str
