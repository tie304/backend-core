from enum import Enum
from typing import Optional, List
import sqlalchemy
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from pydantic import BaseModel
from depends import Base


class EmailTrigger(str, Enum):
    signup = "signup"
    password_reset = "password_reset"


class EmailTriggerInput(BaseModel):
    template_id: int
    trigger: EmailTrigger


class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    template_name = Column(String, unique=True)
    object_id = Column(String, unique=True)  # bucket
    trigger = Column(sqlalchemy.Enum(EmailTrigger))
    fields = Column(ARRAY(String))  # fields pulled off template
    field_value_map = Column(MutableDict.as_mutable(JSONB))


class EmailTemplateBase(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    template_name: Optional[int]
    object_name: Optional[int]
    fields: Optional[List]


class FieldValueMapInput(BaseModel):
    template_id: int
    value_map: dict
