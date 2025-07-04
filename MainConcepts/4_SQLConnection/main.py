from fastapi import FastAPI, Depends, status, Response, HTTPException
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

# @app.post('/blog')
# def create(request: Blog, db:Session=Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

@app.get('/get')
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
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#How to override status code
@app.get('/get/{id}', status_code=status.HTTP_200_OK)
def show(id, reponse: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # reponse.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": "id not found"}
        #Here is a smarter way👍
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id not found")
    return blog

##Delete a blog
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {"response":'done'}

##Update a Blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
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
