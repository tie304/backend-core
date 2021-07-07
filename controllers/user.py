from models.user import UserSignup
from controllers.auth import get_password_hash, create_user_verification_url
from mappers.users import create_user


def register_user(user_signup: UserSignup, host: str) -> int:
    hash_pw = get_password_hash(user_signup.password)
    user_id = create_user(user_signup.email, hash_pw).id
    create_user_verification_url(user_id, host)
    return user_id
