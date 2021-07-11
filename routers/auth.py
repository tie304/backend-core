from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from models.user import UserSignup, UserBase, UserPasswordIngress
from models.auth import Token
import controllers.auth as auth_controler
import controllers.user as users_controler


from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id="591373063132-5il667cpkarl97s2e6segb41rd2t85v8.apps.googleusercontent.com",
    client_secret="LET3YuQWCTOjg1j36kq7hRke",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

router = APIRouter()

auth_templates = Jinja2Templates(directory="static/templates/web")


@router.route("/google/login")
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route("/google/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(user_login: UserSignup):
    return auth_controler.authenticate_user(user_login)


@router.post("/signup", status_code=201)
def signup(user_signup: UserSignup) -> int:
    user_id = users_controler.register_user(user_signup)
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


@router.post("/users/create/password/reset/")
def create_reset_password(email: str):
    auth_controler.create_reset_password(email)


@router.get("/users/password/reset/")
def get_reset_password(code: str, request: Request):
    return auth_templates.TemplateResponse(
        "password_reset.html", {"request": request, "code": code}
    )


@router.post("/users/password/reset/", status_code=201)
def reset_password(request: Request, code: str, password: str = Form(...)):
    try:
        auth_controler.reset_password(code, password)
    except ValueError as e:
        return auth_templates.TemplateResponse(
            "password_reset.html",
            {"request": request, "status": "password-error", "code": code},
        )

    return auth_templates.TemplateResponse(
        "password_reset.html", {"request": request, "status": "success"}
    )
