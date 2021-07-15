from typing import List
from fastapi import Depends, HTTPException
from controllers.auth import get_current_active_user
from models.user import UserBase


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserBase = Depends(get_current_active_user)):
        if user.roles is None:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted no role assigned to user",
            )
        if not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted user doesnt have correct role",
            )
