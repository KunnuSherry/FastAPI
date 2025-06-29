from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return { "data": f"This is a blog with title as {request.title}" }

