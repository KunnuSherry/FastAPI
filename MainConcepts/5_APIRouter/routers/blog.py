from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import database
import models
from repository import blog
from typing import List
from sqlalchemy.orm import Session
Blog = schemas.Blog
get_db = database.get_db

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

## Example method for controllers
@router.get('/get' )
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {"response":'done'}

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
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