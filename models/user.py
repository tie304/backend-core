import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import expression, func
from pydantic import BaseModel
from depends import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, server_default=expression.false())
    verified = Column(Boolean, server_default=expression.false())
    created_on = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)


class UserVerifed(Base):
    __tablename__ = "user_verification_map"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    code = Column(String)


class UserBase(BaseModel):
    id: int
    email: str
    hashed_password: str
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


class UserOutput(User):
    hashed_password: str

    class Config:
        orm_mode = True
