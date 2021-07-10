from fastapi import HTTPException
from models.user import UserSignup
from controllers.auth import (
    get_password_hash,
    create_user_verification_url,
    check_if_valid_email,
    validate_password,
)
from mappers.users import create_user


def register_user(user_signup: UserSignup) -> int:
    if not check_if_valid_email(user_signup.email):
        raise HTTPException(status_code=400, detail="Incorrect email format")

    validate_password(user_signup.password)
    hash_pw = get_password_hash(user_signup.password)
    user_id = create_user(user_signup.email, hash_pw).id
    create_user_verification_url(user_id)
    return user_id
