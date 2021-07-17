from typing import Optional, List
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, DateTime
from pydantic import BaseModel
from depends import Base


class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    template_name = Column(String, unique=True)
    object_id = Column(String, unique=True)  # bucket
    fields = Column(ARRAY(String))  # fields pulled off template


class EmailTemplateValueMap(Base):
    __tablename__ = "email_template_value_map"
    template_id = user_id = Column(
        Integer, ForeignKey("email_templates.id"), primary_key=True
    )
    value = Column(String, nullable=False)
    field = Column(String, nullable=False)


class EmailTemplateBase(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    template_name: Optional[int]
    object_name: Optional[int]
    fields: Optional[List]

class FieldValueMapInput(BaseModel):
    template_id: int
    value_map: dict
