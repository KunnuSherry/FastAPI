from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Token import verify_token  # ✅ Import the verify_token function

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)  # ✅ Pass token and exception
