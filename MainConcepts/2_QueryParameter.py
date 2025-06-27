from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get('/blog') 
def index(limit=10, published : bool = True, sort: Optional[str] = None): ## Default values are set
    if published:
        return {"data": f'{limit} blogs from database'}

## Would be passed like this: http://127.0.0.1:8000/blog?limit=10&published=false