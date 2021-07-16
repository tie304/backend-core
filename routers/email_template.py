from fastapi import APIRouter, Depends, File, UploadFile

import controllers.email_template as email_template_controler

router = APIRouter()


@router.post("/email_templates/create")
def create_email_template(file: UploadFile = File(...)):
    email_template_controler.create_email_template(file)
    return {"filename": file.filename}
