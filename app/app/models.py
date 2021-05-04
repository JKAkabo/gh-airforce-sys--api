from typing import Optional
from uuid import uuid1
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel

from .db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid1)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    wing = Column(String)
    rank = Column(String)
    hashed_password = Column(String)
    is_superuser: bool = False


class UserIn(User):
    # __tablename__ = "users"
    # password: str
    pass


class UserOut(User):
    key: str
    created_at: float
    updated_at: Optional[float]


# class User(UserIn, UserOut):
#     deleted_at: Optional[float]

