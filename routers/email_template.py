from fastapi import APIRouter, Depends, File, UploadFile

import controllers.email_template as email_template_controler
import controllers.auth as auth_controller

from models.user import UserBase
from models.email_template import FieldValueMapInput, EmailTriggerInput

router = APIRouter()


@router.post("/email_template/create")
def create_email_template(
    file: UploadFile = File(...),
    current_user: UserBase = Depends(auth_controller.get_current_active_user),
):
    return email_template_controler.create_email_template(file, current_user)


@router.post("/email_template/fields")
def update_or_create_value_map(
    value_map: FieldValueMapInput,
    current_user: UserBase = Depends(auth_controller.get_current_active_user),
):
    email_template_controler.update_or_create_value_map(value_map)


@router.get("/email_template")
def get_email_template_by_id(template_id: int):
    return email_template_controler.get_by_id(template_id)


@router.post("/email_template/trigger")
def set_email_trigger(trigger: EmailTriggerInput):

    email_template_controler.set_email_trigger(trigger)
