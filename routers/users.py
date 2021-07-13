from fastapi import APIRouter, Depends
from models.user import UserRoles
from utils.role_checker import RoleChecker
import controllers.user as users_controler

router = APIRouter()

allow_admin_access = RoleChecker([UserRoles.ADMIN.value])


@router.post(
    "/users/disable/", status_code=200, dependencies=[Depends(allow_admin_access)]
)
def disable_user(user_id: int):
    users_controler.disable_user(user_id)
