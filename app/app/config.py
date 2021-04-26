import os
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    # POSTGRES_SERVER:
    # POSTGRES_USER: os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://bookmarks:edem1234@/airforce"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            path=f"/{os.getenv('POSTGRES_DB') or ''}"
        )

    class Config:
        case_sensitive: True
        env_file = '.env'


settings = Settings()

