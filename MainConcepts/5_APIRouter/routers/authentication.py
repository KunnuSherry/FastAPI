from fastapi import APIRouter, Depends, status, HTTPException
import schemas
from fastapi.security import OAuth2PasswordRequestForm
import database
import models
from sqlalchemy.orm import Session
from hashing_password import verify
from Token import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user or not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
