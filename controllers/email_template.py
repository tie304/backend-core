import io
import re
from fastapi import File, HTTPException
from controllers.s3 import upload_file


def validate_email_template(file: File):
    if not file.filename.endswith(".html"):
        raise HTTPException(
            status_code=400, detail="incorrect file format please upload an HTML file"
        )


def extract_fields(file: bytes):
    fields = []
    res = re.findall(r"\{{.*?\}}", str(file))
    for field in res:
        field = field.replace("{", "")
        field = field.replace("}", "")
        fields.append(field)
    return fields


def create_email_template(file: File):
    data = file.file.read()
    validate_email_template(file)
    fields = extract_fields(data)
    upload_data = io.BytesIO(data)
    file_id = upload_file(upload_data)
    # TODO create email template object
    # TODO create fields mapping to template object
