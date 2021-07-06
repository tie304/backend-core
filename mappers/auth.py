from depends import get_database
from models.user import UserVerifed, User


def create_user_verification_url(user_id: int, code: str) -> None:
    session = get_database()
    db_verified = UserVerifed(user_id=user_id, code=code)
    session.add(db_verified)
    session.commit()
    session.close()


def get_user_verification(code: str) -> None:
    session = get_database()
    verifed_map = session.query(UserVerifed).filter(UserVerifed.code == code).first()
    session.close()
    return verifed_map
