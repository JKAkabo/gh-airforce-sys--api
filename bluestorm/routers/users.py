from datetime import datetime

from bluestorm.dependencies import AppContext, get_app_context, get_crypt_context, get_current_user
from bluestorm.models.users import UserIn, UserOut, User
from databases.backends.postgres import Record
from deta import Deta
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=list[UserOut])
async def read_users(app_context: AppContext = Depends(get_app_context)):
    base = app_context.deta.Base('users')
    return next(base.fetch())
 

@router.get('/me', response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/{user_key}', response_model=UserOut)
async def read_user(user_key: str, app_context: AppContext = Depends(get_app_context)):
    base = app_context.deta.Base('users')
    return base.get(user_key)


@router.post('', response_model=UserOut)
async def create_user(userIn: UserIn, app_context: AppContext = Depends(get_app_context)):
    base = app_context.deta.Base('users')
    user = userIn.dict()
    user['password'] = get_crypt_context().hash(user['password'])
    user['created_at'] = datetime.now().timestamp()
    return base.put(user);


@router.put('/{user_key}', response_model=UserOut)
async def update_user(user_key: str, userIn: UserIn, app_context: AppContext = Depends(get_app_context)):
    base = app_context.deta.Base('users')
    user = userIn.dict()
    user['updated_at'] = datetime.now().timestamp()
    return base.update(user, user_key)
