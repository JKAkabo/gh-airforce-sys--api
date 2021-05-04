from typing import Optional
from pydantic import BaseModel, UUID1


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    wing: Optional[str] = None
    rank: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    first_name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    wing: Optional[str]
    rank: Optional[str]


class HTTPError(BaseModel):
    detail: str


class UserUpdate(User):
    pass


class UserInDBBase(User):
    id: Optional[UUID1] = None

    class Config:
        orm_mode = True
