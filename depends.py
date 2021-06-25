import databases
from sqlalchemy import create_engine

from models.config import DBConfig

cfg = DBConfig()
DATABASE_URL = "postgres://{cfg.database_user:{}cfg.database_password}@batyr.db.elephantsql.com/{cfg.database_por
t}"
class Database:
    engine = create_engine(f"")
    database = databases.Database(DATABASE_URL)
