from typing import Any, List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from . import actions, models, schemas
from .db import SessionLocal, engine

# Create all tables in the database.
# Comment this out if you using migrations.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Hello world!"}


@app.get("/users", response_model=List[schemas.User], tags=["users"])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    users = actions.user.get_all(db=db, skip=skip, limit=limit)
    return users


@app.post("/users", response_model=schemas.User, status_code=HTTP_201_CREATED, tags=["users"])
def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate) -> Any:
    user = actions.user.create(db=db, obj_in=user_in)
    return user


@app.put("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"],)
def update_user(*, db: Session = Depends(get_db), id: UUID4, user_in: schemas.UserUpdate,) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
    user = actions.user.update(db=db, db_obj=user, obj_in=user_in)
    return user


@app.get("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"],)
def get_user(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.delete("/users/{id}", response_model=schemas.User, responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}}, tags=["users"], )
def delete_user(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    user = actions.user.remove(db=db, id=id)
    return user


