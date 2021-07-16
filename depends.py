import boto3
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.config import DBConfig, Config, AWSConfig


cfg = DBConfig()
aws_cfg = AWSConfig()
DATABASE_URL = f"postgres://{cfg.database_user}:{cfg.database_password}@{cfg.database_host}/{cfg.database_name}"

Base = declarative_base()


class Database:
    engine = None
    database = None
    session_maker = None

    def __init__(self):
        Database.engine = create_engine(DATABASE_URL)
        Database.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=Database.engine
        )
        Base.metadata.create_all(bind=Database.engine)
        logging.info("tables created")


def get_s3_client():
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_cfg.access_key,
        aws_secret_access_key=aws_cfg.secret_key,
    )
    return client


def get_database():
    # Dependency
    db = Database.session_maker()
    return db


def get_config() -> Config:
    return Config()
