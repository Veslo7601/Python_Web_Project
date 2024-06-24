from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
<<<<<<< HEAD
    # redis_password: str = "password"
=======
    redis_password: str = "password"
    CLD_NAME: str = "diho9zuth"
    CLD_API_KEY: str = "833657613867498"
    CLD_API_SECRET: str = "xV67Lwc7AG_7JHqjyix77S5Hf8A"
>>>>>>> 0f3fa55 (crud for images, requirements, redis password)

    model_config = ConfigDict(extra='ignore', env_file='.env', env_file_encoding="utf-8")  # noqa


settings = Settings()
