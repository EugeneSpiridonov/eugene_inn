from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: int
    DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: int
    TEST_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_PASS: str
    REDIS_HOST: str
    REDIS_PORT: int
    MODE: Literal["DEV", "TEST", "PROD"]

    class Config:
        env_file = ".env"


settings = Settings()
