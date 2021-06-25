from pydantic import BaseSettings


class DBConfig(BaseSettings):
    database_name: str = "wxvdgvep"
    database_user: str = "wxvdgvep"
    database_password: str = "L0LiZ3hqkw5lKBH5W8F2A1kLa-Kt80A7"
    database_host: str = "batyr.db.elephantsql.com"
    database_port: int = 5432

