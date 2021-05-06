from datetime import datetime, timedelta
from typing import Optional, Any, List
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from .schemas import Token, TokenData, User, UserInDB, UserCreate
from .db.session import SessionLocal
from . import actions

# alembic revision --autogenerate -m "Create user table"
# alembic upgrade head

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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user



async def get_current_user(token: str = Depends(oauth2_scheme)):

    user = fake_decode_token(token)

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid authentication credentials",

            headers={"WWW-Authenticate": "Bearer"},

        )

    return user





async def get_current_active_user(current_user: User = Depends(get_current_user)):

    if current_user.disabled:

        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):

    return current_user





@app.get("/login/")
async def login_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/")
def index():
    return {"message": "Hello world!"}


@app.get("/users", response_model=List[User], tags=["users"])
def list_users(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    users = actions.user.get_all(db=db, skip=skip, limit=limit)
    return users


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
