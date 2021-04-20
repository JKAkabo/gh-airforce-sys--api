from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from bluestorm.dependencies import get_crypt_context, get_app_context, AppContext
from bluestorm.models.access_tokens import AccessToken
from bluestorm.models.users import User

router = APIRouter(prefix='/access-tokens', tags=['access_tokens'])


@router.post('', response_model=AccessToken)
async def create_access_token(credentials: OAuth2PasswordRequestForm = Depends(), app_context: AppContext = Depends(get_app_context)):
    base = app_context.deta.Base('users')
    users: list[User] = next(base.fetch({'email': credentials.username}))
    print(users)
    if not users or not get_crypt_context().verify(credentials.password, users[0]['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if users[0]['disabled']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Account Disabled',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = {
        'sub': users[0]['key'],
        'exp': (datetime.now() + timedelta(hours=4)).timestamp()
    }
    return {
        'access_token': jwt.encode(payload, app_context.settings.SECRET_KEY, 'HS256')
    }