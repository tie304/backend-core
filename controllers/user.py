from models.user import UserSignup
from controllers.auth import get_password_hash
from mappers.users import create_user

def register_user(user_signup: UserSignup) -> int:
    hash_pw = get_password_hash(user_signup.password)
    user_id = create_user(user_signup.email, hash_pw)
    return user_id
    
