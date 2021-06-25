from depends import get_db
from models.user import User

def create_user(email: str, hashed_password: str) -> int:
    db = get_db()
    
    db.cur.execute(f"INSERT INTO users (email, password) VALUES ('{email}', '{hashed_password}') RETURNING user_id;")
    return db.cur.fetchone()[0]
