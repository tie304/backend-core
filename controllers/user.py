from fastapi import HTTPException
from models.user import UserSignup, UserBase
from controllers.auth import (
    get_password_hash,
    create_user_verification_url,
    check_if_valid_email,
    validate_password,
)
import mappers.users as users_mapper


def register_user(user_signup: UserSignup) -> int:
    if not check_if_valid_email(user_signup.email):
        raise HTTPException(status_code=400, detail="Incorrect email format")

    validate_password(user_signup.password)
    hash_pw = get_password_hash(user_signup.password)
    user_id = users_mapper.create_user(user_signup.email, hash_pw).id
    create_user_verification_url(user_id)
    return user_id


def disable_user(user_id: int):
    user = users_mapper.get_user_by_id(user_id)
    user.disabled = True
    users_mapper.update_user(user)
