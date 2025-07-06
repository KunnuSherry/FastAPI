from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import database
import models
from typing import List
from hashing_password import hash_password
from sqlalchemy.orm import Session
User = schemas.User
get_db = database.get_db
ShowUser = schemas.ShowUser

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

#Creating User
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: User, db:Session=Depends(get_db)):
    hashed_password = hash_password(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user(id:int ,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if(not user):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

