from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PROJECT INFORMATION
    PROJECT_NAME: str = 'NewEra Cash & Carry'
    PROJECT_DESCRIPTION: str = 'This is project which is own NewEra Cash & Carry'
    PROJECT_VERSION: str = '0.0.1'

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # JWT CREDENTIALS
    JWT_ENCRYPT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file='.env')


@cache
def get_settings() -> Settings:
    return Settings()