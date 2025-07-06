from passlib.context import CryptContext

pwd_ctxt = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password: str):
    return pwd_ctxt.hash(password)