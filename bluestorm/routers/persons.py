from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from bluestorm.models.persons import Person, PersonCreate, PersonOut, PasswordResetIn, PasswordResetRequestIn
from bluestorm.dependencies import get_deta, get_settings, get_crypt_context
from deta import Deta
from datetime import datetime
from bluestorm.config import Settings
from jose import jwt, JWTError

router = APIRouter(prefix='/persons', tags=['persons'])


@router.get('', response_model=List[PersonOut])
async def read_persons(deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    return next(base.fetch())


@router.get('/{person_key}', response_model=PersonOut)
async def read_person(person_key: str, deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    return base.get(person_key)


@router.post('', response_model=PersonOut)
async def create_person(person_in: PersonCreate, deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    person = person_in.dict()
    person['created_at'] = datetime.now().timestamp()
    person['updated_at'] = None
    person['deleted_at'] = None
    return base.put(person)


@router.post('/{person_key}/password-reset-request')
async def request_password_reset(person_key: str, password_request_reset_in: PasswordResetRequestIn, deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    person = base.get(person_key)
    # person[]

@router.put('/{person_key}', response_model=PersonOut)
async def update_person(person_key: str, person_in: PersonCreate, deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    person = person_in.dict()
    person['updated_at'] = datetime.now().timestamp()
    return base.update(person, person_key)


@router.put('/{person_key}/password', response_model=PersonOut)
async def reset_password_for_person(person_key: str, password_reset_in: PasswordResetIn, deta: Deta = Depends(get_deta), settings: Settings = Depends(get_settings)):
    password_reset_failed_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Password Reset Failed')
    payload = {}
    base = deta.Base('users')
    try:
        payload = jwt.decode(password_reset_in.token, settings.SECRET_KEY, 'HS256')
    except JWTError:
        raise password_reset_failed_exception
    key: str = payload.get('sub')
    if key is None:
        raise password_reset_failed_exception
    users = next(base.fetch({'key': key, 'can_login': True, 'deleted_at': None}))
    if not users:
        raise password_reset_failed_exception
    users[0]['password'] = get_crypt_context().hash(password_reset_in.password)
    return base.put(users[0])


@router.delete('/{person_key}', response_model=None)
async def delete_person(person_key: str, deta: Deta = Depends(get_deta)):
    base = deta.Base('persons')
    person = base.get(person_key)
    person['deleted_at'] = datetime.now().timestamp()
    base.put(person)
    return None
