from typing import List
from fastapi import Depends, HTTPException
from controllers.auth import get_current_active_user
from models.user import UserBase


class RoleChecker:
    """
    Assumes user has role attribute

    """

    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserBase = Depends(get_current_active_user)):
        if not user.role:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted no role assigned to user",
            )
        if not user.role in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted user doesnt have correct role",
            )
