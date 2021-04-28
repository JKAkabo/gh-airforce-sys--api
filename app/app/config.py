import os
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator

# personnel can create a personnel
# fname, lname,wing, id(key)
# Wings table and wing (1:1) Relationship
# Ranks Categories (Enlisted Ranks, Warrant Ranks, )
# Ranks ( )
# Personnel (those who can login with super access )
# Admin account. Can add other users. CRUD users.
# View all personnel data
# Record duty post, leave, operations for every user


class Settings(BaseSettings):

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

