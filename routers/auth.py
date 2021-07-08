from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from models.user import UserSignup, UserBase, UserPasswordIngress
from models.auth import Token
import controllers.auth as auth_controler
import controllers.user as users_controler

router = APIRouter()

auth_templates = Jinja2Templates(directory="static/templates/web")


@router.post("/token", response_model=Token)
def login_for_access_token(user_login: UserSignup):
    return auth_controler.authenticate_user(user_login)


@router.post("/signup", status_code=201)
def signup(user_signup: UserSignup, request: Request) -> int:
    host = request.client.host
    user_id = users_controler.register_user(user_signup, host)
    return user_id


@router.get("/users/me/", response_model=UserBase)
def read_users_me(
    current_user: UserBase = Depends(auth_controler.get_current_active_user),
):
    return current_user


@router.get("/users/verify/")
def verify(code: str, request: Request):
    auth_controler.verify_user(code)
    return auth_templates.TemplateResponse("verification.html", {"request": request})


@router.post("/users/password/reset/")
def create_reset_password(email: str):
    auth_controler.create_reset_password(email)


@router.put("/users/password/reset/", status_code=201)
def reset_password(code: str, user_password: UserPasswordIngress):
    auth_controler.reset_password(code, user_password)
