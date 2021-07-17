import io
import re
from fastapi import File, HTTPException
from controllers.s3 import upload_file
from controllers.auth import get_current_active_user
import mappers.email_template as email_template_mapper
from models.user import UserBase
from models.email_template import FieldValueMapInput

def validate_field_value_map(fields: list, value_map: dict):
    for item in value_map.keys():
        if item not in fields:
            raise HTTPException(status_code=400, detail="incorrct field provided")

def validate_email_template(file: File):
    if not file.filename.endswith(".html"):
        raise HTTPException(
            status_code=400, detail="incorrect file format please upload an HTML file"
        )


def extract_fields(file: bytes):
    """
    Extracts fields containing {{value}} in text and then removes '{' '}' chars
    """
    fields = []
    res = re.findall(r"\{{.*?\}}", str(file))
    for field in res:
        field = field.replace("{", "")
        field = field.replace("}", "")
        fields.append(field)
    return fields


def create_email_template(file: File, current_user: UserBase):
    data = file.file.read()
    validate_email_template(file)
    fields = extract_fields(data)
    upload_data = io.BytesIO(data)
    file_id = upload_file(upload_data)
    return email_template_mapper.create_email_template(template_name=file.filename, user_id = current_user.id, object_id=file_id, fields=fields)

def update_or_create_value_map(value_map_input: FieldValueMapInput):
    template = email_template_mapper.get_by_id(value_map_input.template_id)
    fields = template.fields
    validate_field_value_map(fields, value_map_input.value_map)
    
