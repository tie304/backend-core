from typing import Optional, List
from fastapi import APIRouter, Depends
from models.user import UserRoles
from utils.role_checker import RoleChecker
from models.user import UserOutput, User
import controllers.user as users_controler

router = APIRouter()

allow_admin_access = RoleChecker([UserRoles.ADMIN.value])


@router.post(
    "/users/disable/", status_code=200, dependencies=[Depends(allow_admin_access)]
)
def disable_user(user_id: int):
    users_controler.disable_user(user_id)


@router.post(
    "/users/enable",
    response_model=List[UserOutput],
    status_code=200,
    dependencies=[Depends(allow_admin_access)],
)
def enable_user(user_id: int):
    users_controler.enable_user(user_id)


@router.get(
    "/users/search", status_code=200, dependencies=[Depends(allow_admin_access)]
)
def users_search(limit: int, skip: int):
    return users_controler.search(limit=limit, skip=skip)
