from typing import Optional
from pydantic import BaseModel, UUID4


class HTTPError(BaseModel):
    detail: str


# Shared Properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    wing: Optional[str] = None
    rank: Optional[str] = None


class User(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[str] = None


class UserInDB(User):
    hashed_password: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: str
    last_name: str
    wing: str
    rank: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[UUID4] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB




