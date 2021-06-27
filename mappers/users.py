from models.user import User, users_table
from depends import get_database


async def create_user(email: str, hashed_password: str) -> int:
    db = get_database()
    query = users_table.insert().values(
        email=email, hashed_password=hashed_password, disabled=False
    )
    last_record_id = await db.execute(query)


async def get_user_by_email(email: str) -> User:
    db = get_database()
    query = users_table.select().where(users_table.c.email == email)
    user = await db.fetch_one(query=query)
    return _query_to_model(tuple(user.keys()), tuple(user.values()))


def _query_to_model(keys: tuple, values: tuple) -> User:
    return User(**dict(zip(keys, values)))
