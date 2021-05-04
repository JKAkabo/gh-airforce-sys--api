from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .schemas import Token, TokenData, User, UserInDB
from .db.session import SessionLocal

SECRET_KEY = "0d785176a0ed6bcc8dd2783f86fd6786e6ac105e9de743294deddbef0c60eda3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "wing": "Many",
        "rank": "Captain",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

#
#
# from typing import Any, List, Optional
#
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#
# from pydantic import UUID4, BaseModel
# from jose impor JWTError, jwt
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
#
#
# SECRET_KEY = "d7bd748358b88c63c084ecacc0efdbf221d5d64e60939ae5111811329aeb8a83"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRES_MINUTES = 30
#
#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "first_name": "John Doe",
#         "last_name": "johndoe",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "last_name": "alice",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }
#
#
#
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# app = FastAPI()
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @app.get("/login/")
# async def login_user(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


@app.get("/")
def index():
    return {"message": "Hello world!"}


# @app.get("/users", response_model=List[schemas.User], tags=["users"])
# def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
#     users = actions.user.get_all(db=db, skip=skip, limit=limit)
#     return users
#
#
# @app.post("/users", response_model=schemas.User, status_code=HTTP_201_CREATED, tags=["users"])
# def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate) -> Any:
#     user = actions.user.create(db=db, obj_in=user_in)
#     return user
#
#
# @app.put("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"],)
# def update_user(*, db: Session = Depends(get_db), id: UUID4, user_in: schemas.UserUpdate,) -> Any:
#     user = actions.user.get(db=db, id=id)
#     if not user:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
#     user = actions.user.update(db=db, db_obj=user, obj_in=user_in)
#     return user
#
#
# @app.get("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"],)
# def get_user(*, db: Session = Depends(get_db), id: UUID4) -> Any:
#     user = actions.user.get(db=db, id=id)
#     if not user:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
#     return user
#
#
# @app.delete("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"], )
# def delete_user(*, db: Session = Depends(get_db), id: UUID4) -> Any:
#     user = actions.user.get(db=db, id=id)
#     if not user:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
#     user = actions.user.remove(db=db, id=id)
#     return user
#
#
