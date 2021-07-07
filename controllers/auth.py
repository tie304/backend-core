import os
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import UserBase, UserOutput, UserSignup, UserPasswordIngress
from models.auth import TokenData
from models.config import AuthConfig

from mappers.users import get_user_by_email, get_user_by_id, update_user
import mappers.auth as auth_mapper

cfg = AuthConfig()

# openssl rand -hex 32
SECRET_KEY = cfg.jwt_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = cfg.token_expire


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_random_code(N: int = 15) -> str:
    # initializing size of string

    # using random.choices()
    # generating random strings
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return res


def create_user_verification_url(user_id: int):
    code = generate_random_code()
    auth_mapper.create_user_verification_url(user_id, code)


def verify_user(code: str):
    user_map = auth_mapper.get_user_verification(code)
    if not user_map:
        raise HTTPException(status_code=400, detail="incorrect code provided")
    user = get_user_by_id(user_map.user_id)
    if user.verified:
        raise HTTPException(status_code=400, detail="user already verified")
    user.verified = True
    update_user(user)
    auth_mapper.delete_user_verification_by_code(code)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserOutput(**user_dict)


def authenticate_user(user_login: UserSignup):
    user = validate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def validate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # extract data pulled off user
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_reset_password(email: str):
    user = get_user_by_email(email)
    reset = auth_mapper.get_password_reset_by_user_id(user.id)
    if reset:
        # TODO resend code
        return
    if user and user.verified and not user.disabled:
        code = generate_random_code()
        auth_mapper.create_password_reset(user.id, code)
        # TODO send email here


def reset_password(code: str, password: UserPasswordIngress):
    reset = auth_mapper.get_password_reset_by_code(code)
    if not reset:
        raise HTTPException(status_code=401, detail="invalid code")
    user = get_user_by_id(reset.user_id)
    new_hash = get_password_hash(password.password)
    user.hashed_password = new_hash
    update_user(user)
    auth_mapper.delete_password_reset_by_code(code)
