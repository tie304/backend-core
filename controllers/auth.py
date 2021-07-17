import os
import re
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import User, UserBase, UserOutput, UserSignup, UserPasswordIngress
from models.auth import TokenData
from models.config import AuthConfig, ProductConfig

from mappers.users import get_user_by_email, get_user_by_id, update_user
import mappers.auth as auth_mapper
import controllers.email as email_controller

cfg = AuthConfig()
prod_cfg = ProductConfig()
# openssl rand -hex 32
SECRET_KEY = cfg.jwt_key
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_if_valid_email(email: str) -> bool:
    exp = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    # and the string in search() method
    if re.match(exp, email):
        return True
    return False


def generate_random_code(N: int = 15) -> str:
    # initializing size of string

    # using random.choices()
    # generating random strings
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return res


def validate_password(password: str):
    if len(password) < cfg.password_length:
        raise ValueError("password must be {cfg.password_length}")


def create_user_verification_url(user_id: int):
    code = generate_random_code()
    auth_mapper.create_user_verification_url(user_id, code)
    user = get_user_by_id(user_id)
    verify_url = f"{prod_cfg.product_ingress_host}/users/verify?code={code}"
    email_controller.send_verification_email(user.email, verify_url)


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


def authenticate_user(user_login: UserSignup):
    user = validate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_token(user.email)
    refresh_token = encode_refresh_token(user.email)

    return {"access_token": access_token, "refresh_token": refresh_token}


def encode_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=0, hours=cfg.access_token_expire),
        "iat": datetime.utcnow(),
        "scope": "access_token",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def encode_refresh_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=0, hours=cfg.refresh_token_expire),
        "iat": datetime.utcnow(),
        "scope": "refresh_token",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "refresh_token":
            email = payload["sub"]
            new_token = encode_token(email)
            return new_token
        raise HTTPException(status_code=401, detail="Invalid scope for token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def decode_token(self, token):
    try:
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        if payload["scope"] == "access_token":
            return payload["sub"]
        raise HTTPException(status_code=401, detail="Scope for the token is invalid")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def validate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


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
    if reset:  # if reset entry already found then resend email with same code
        reset_url = (
            f"{prod_cfg.product_ingress_host}/users/password/reset/?code={reset.code}"
        )
        email_controller.send_password_reset_email(email, reset_url)
        return
    if user and user.verified and not user.disabled:
        code = generate_random_code()
        auth_mapper.create_password_reset(user.id, code)
        reset_url = f"{prod_cfg.product_ingress_host}/users/password/reset/?code={code}"
        email_controller.send_password_reset_email(email, reset_url)
        return
    raise HTTPException(status_code=400, detail="Please verify your email first")


def reset_password(code: str, password: str):
    reset = auth_mapper.get_password_reset_by_code(code)
    if not reset:
        raise HTTPException(status_code=401, detail="invalid code")
    validate_password(password)
    user = get_user_by_id(reset.user_id)
    new_hash = get_password_hash(password)
    user.hashed_password = new_hash
    update_user(user)
    auth_mapper.delete_password_reset_by_code(code)
