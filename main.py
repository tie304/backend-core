from fastapi import Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel

from models.user import UserBase, UserSignup
from depends import Database, get_database
from routers import auth

app = FastAPI()

Database()  # init database

app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass
