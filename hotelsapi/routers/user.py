from fastapi import Depends, APIRouter, Query, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, utils
from ..schemas import users
from ..database import get_db

from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=users.UserOut)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):

    #  Hash user password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("",  response_model=List[users.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model=users.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} not found")

    return user


@router.put("/{id}")
def update_user():
    pass


@router.delete("/{id}")
def remove_user():
    pass
