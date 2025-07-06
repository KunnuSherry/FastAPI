import models
from sqlalchemy.orm import Session
import database
from fastapi import Depends

def get_all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
