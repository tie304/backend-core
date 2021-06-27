import databases
import logging
from sqlalchemy import create_engine, MetaData

from models.config import DBConfig

cfg = DBConfig()
DATABASE_URL = f"postgres://{cfg.database_user}:{cfg.database_password}@{cfg.database_host}/{cfg.database_name}"


metadata = MetaData()


class Database:
    engine = None
    database = None

    def __init__(self):
        Database.engine = create_engine(DATABASE_URL)
        Database.database = databases.Database(DATABASE_URL)
        metadata.create_all(Database.engine)
        logging.info("tables created")


def get_database():
    return Database.database
