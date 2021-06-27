from fastapi import Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel

from models.auth import Token
from models.user import User, UserSignup
from controllers.auth import *
import controllers.user as users_controler
from depends import Database, get_database


app = FastAPI()

Database()  # init database


@app.on_event("startup")
async def startup():
    print("starting up")
    database = get_database()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    database = get_database()
    await database.disconnect()


@app.post("/token", response_model=Token)
async def login_for_access_token(user_login: UserSignup):
    user = await authenticate_user(user_login.email, user_login.password)
    print("user here")
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


@app.post("/signup", status_code=201)
async def signup(user_signup: UserSignup):
    user_id = await users_controler.register_user(user_signup)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
