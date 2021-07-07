from pydantic import BaseSettings


class DBConfig(BaseSettings):
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int = 5432


class AuthConfig(BaseSettings):
    jwt_key: str
    token_expire: int = 120


class SendGridConfig(BaseSettings):
    sendgrid_api_key: str


class ProductConfig(BaseSettings):
    product_name: str = "Product name here"
