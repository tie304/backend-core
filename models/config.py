from typing import Optional
from pydantic import BaseSettings, BaseModel

# ENV SETTINGS
class DBConfig(BaseSettings):
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int = 5432


class AuthConfig(BaseSettings):
    jwt_key: str
    token_expire: int = 120  # minutes
    password_length: int = 6


class SendGridConfig(BaseSettings):
    sendgrid_api_key: str
    sendgrid_sender: str  # verified sender email


class ProductConfig(BaseSettings):
    product_name: str
    product_ingress_host: str


class Config(BaseModel):
    db: DBConfig = DBConfig()
    basic_auth: AuthConfig = AuthConfig()
    sendgrid: SendGridConfig = SendGridConfig()
    product_config: ProductConfig = ProductConfig()


class EmailSettings(BaseModel):
    verify_header: str = "Welcome!"
    verify_subtext: str = "To get started please verify your email!"
    company_name: Optional[str]
    company_address_1: Optional[str]
    company_address_2: Optional[str]
