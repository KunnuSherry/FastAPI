from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog, User, ShowUser
from database import engine, SessionLocal
import models
app = FastAPI()
from sqlalchemy.orm import Session
from hashing_password import hash_password
from database import get_db
from routers import blog
from routers import user

app = FastAPI()



models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)