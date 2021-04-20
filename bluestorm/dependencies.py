from functools import lru_cache
import asyncpg
from deta import Deta
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from bluestorm.config import Settings
from passlib.context import CryptContext
from jose import jwt, JWTError
from bluestorm.models.users import User
from bluestorm.models.persons import Person
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='access-tokens')

class AppContext:
    deta: Deta
    settings: Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_deta() -> Deta:
    settings: Settings = get_settings()
    return Deta(settings.DETA_KEY)


@lru_cache()
def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    print('token')
    settings: Settings = get_settings()
    deta: Deta = get_deta()
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, 'HS256')
        key: str = payload.get('sub')
        if key is None:
            return None
        user = deta.Base('users').get(key)
        return User(**user)
    except JWTError:
        return None


async def get_app_context() -> AppContext:
    app_context = AppContext()
    app_context.deta = get_deta()
    app_context.settings = get_settings()
    return app_context


async def request_password_reset(person: Person) -> None:
    pass


async def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool
