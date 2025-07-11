from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog, User, ShowUser
from database import engine, SessionLocal
import models
app = FastAPI()
from sqlalchemy.orm import Session
from hashing_password import hash_password
from database import get_db

models.Base.metadata.create_all(engine)

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post('/blog')
# def create(request: Blog, db:Session=Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

@app.get('/get' ,tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# @app.get('/get/{id}')
# def show(id, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id==id).first()
#     return blog


########################################################################
#Response Codes

# @app.post('/blog', status_code=201)
# def create(request: Blog, db:Session=Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog


## Smarter Way to do this
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#How to override status code
# @app.get('/get/{id}', status_code=status.HTTP_200_OK)
# def show(id, reponse: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id==id).first()
#     if not blog:
#         # reponse.status_code = status.HTTP_404_NOT_FOUND
#         # return {"detail": "id not found"}
#         #Here is a smarter way👍
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id not found")
#     return blog

##Delete a blog
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {"response":'done'}

##Update a Blog
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    try:
        blog_query = db.query(models.Blog).filter(models.Blog.id == id)

        if blog_query.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with given ID not found")

        blog_query.update(request.dict(), synchronize_session=False)
        db.commit()
        return {"message": "Blog updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Update failed: {str(e)}")


#Response Model (We will not get id)
@app.get('/get/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog ,tags=['blogs'])
def show(id, reponse: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # reponse.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": "id not found"}
        #Here is a smarter way👍
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id not found")
    return blog


#####################################################################################################

#Creating User
@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
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

@app.get('/user/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK, tags=['users'])
def get_user(id:int ,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if(not user):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

## The tags can be used to distinguish the blogs and user routes in swagger UI