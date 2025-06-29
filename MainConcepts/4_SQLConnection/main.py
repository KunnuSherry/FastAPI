from fastapi import FastAPI, Depends
from schemas import Blog
from database import engine, SessionLocal
import models
app = FastAPI()
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog