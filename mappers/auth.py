from depends import get_database
from models.user import UserVerifed, User, UserPasswordReset


def create_user_verification_url(user_id: int, code: str) -> None:
    session = get_database()
    db_verified = UserVerifed(user_id=user_id, code=code)
    session.add(db_verified)
    session.commit()
    session.close()


def get_user_verification(code: str) -> UserVerifed:
    session = get_database()
    verifed_map = session.query(UserVerifed).filter(UserVerifed.code == code).first()
    session.close()
    return verifed_map


def delete_user_verification_by_code(code: str):
    session = get_database()
    session.query(UserVerifed).filter(UserVerifed.code == code).delete()
    session.commit()
    session.close()


def create_password_reset(user_id: int, code: str) -> None:
    session = get_database()
    db_verified = UserPasswordReset(user_id=user_id, code=code)
    session.add(db_verified)
    session.commit()
    session.close()


def get_password_reset_by_code(code: str) -> UserPasswordReset:
    session = get_database()
    reset = (
        session.query(UserPasswordReset).filter(UserPasswordReset.code == code).first()
    )
    session.close()
    return reset


def get_password_reset_by_user_id(_id: str) -> UserPasswordReset:
    session = get_database()
    reset = (
        session.query(UserPasswordReset)
        .filter(UserPasswordReset.user_id == _id)
        .first()
    )
    session.close()
    return reset


def delete_password_reset_by_code(code: str):
    session = get_database()
    session.query(UserPasswordReset).filter(UserPasswordReset.code == code).delete()
    session.commit()
    session.close()
