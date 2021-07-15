import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import expression, func
from pydantic import BaseModel
from depends import Base


class UserRoles(Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    roles = Column(ARRAY(String))
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


class UserBase(BaseModel):
    id: int
    email: str
    roles: List[UserRoles]
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
    roles: List[UserRoles] = []
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
