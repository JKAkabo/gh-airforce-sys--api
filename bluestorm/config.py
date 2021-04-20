from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DETA_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'
