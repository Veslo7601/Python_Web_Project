from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    
    secret_key: str = "secret"
    algorithm: str = "HS256"

    mail_username: str = "veslo7601@meta.ua"
    mail_password: str = "Q12345Rr"
    mail_from: str = "veslo7601@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"


    # redis_host: str = "localhost"
    # redis_port: int = 6379
    # # redis_password: str = "password"

    model_config = ConfigDict(extra='ignore', env_file='.env', env_file_encoding="utf-8")  # noqa


settings = Settings()
