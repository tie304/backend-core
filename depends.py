import databases
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.config import DBConfig, Config

cfg = DBConfig()
DATABASE_URL = f"postgres://{cfg.database_user}:{cfg.database_password}@{cfg.database_host}/{cfg.database_name}"

Base = declarative_base()


class Database:
    engine = None
    database = None
    session_maker = None

    def __init__(self):
        Database.engine = create_engine(DATABASE_URL)
        Database.database = databases.Database(DATABASE_URL)
        Database.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=Database.engine
        )
        Base.metadata.create_all(bind=Database.engine)
        logging.info("tables created")


def get_database():
    # Dependency
    db = Database.session_maker()
    return db


def get_config() -> Config:
    return Config()
