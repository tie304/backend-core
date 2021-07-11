from fastapi import Depends, FastAPI, HTTPException, status, Response
from models.user import UserBase, UserSignup
from starlette.middleware.sessions import SessionMiddleware
from depends import Database, get_database
from routers import auth

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")
Database()  # init database

app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/healthcheck", status_code=200)
def healthcheck():
    pass
