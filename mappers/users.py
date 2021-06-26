from models.user import User, users_table
from depends import get_database


async def create_user(email: str, hashed_password: str) -> int:
    db = get_database()
    query = users_table.insert().values(
        email=email, hashed_password=hashed_password, disabled=False
    )
    print(query, "query here")
    last_record_id = await db.execute(query)
    print(last_record_id)
