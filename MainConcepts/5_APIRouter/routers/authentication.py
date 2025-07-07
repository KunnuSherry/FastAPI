from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import database
import models
from sqlalchemy.orm import Session
from hashing_password import verify

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def login(request: schemas.Login, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    return user