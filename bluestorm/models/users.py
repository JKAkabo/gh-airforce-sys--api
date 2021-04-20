from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .base import BluestormModel


class UserBase(BluestormModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = Field(min_length=10, max_length=10)
    is_superuser: bool = False
    disabled: bool = False


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    key: str
    created_at: float
    updated_at: Optional[float]


class User(UserIn, UserOut):
    deleted_at: Optional[float]
