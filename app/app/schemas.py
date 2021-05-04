from typing import Optional
from pydantic import BaseModel, UUID4


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    wing: Optional[str] = None
    rank: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    username: str
    first_name: str
    last_name: str
    wing: str
    rank: str


class HTTPError(BaseModel):
    detail: str


class UserUpdate(User):
    pass


class UserInDBBase(User):
    id: Optional[UUID4] = None

    class Config:
        orm_mode = True
