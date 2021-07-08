import sqlalchemy
from fastapi import Depends, HTTPException
from models.user import User, UserBase
from depends import get_database

from models.user import User


def create_user(email: str, hashed_password: str) -> User:
    session = get_database()
    db_user = User(email=email, hashed_password=hashed_password)
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)
        return db_user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        session.close()


def update_user(user: User) -> None:
    session = get_database()
    session.add(user)
    session.commit()
    session.close()


def get_user_by_email(email: str) -> User:
    session = get_database()
    user = session.query(User).filter(User.email == email).first()
    session.close()
    return user


def get_user_by_id(_id: int) -> User:
    session = get_database()
    user = session.query(User).filter(User.id == _id).first()
    session.close()
    return user
