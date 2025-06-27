from fastapi import FastAPI

app = FastAPI()

@app.get('/') 
def index(): 
    return {"message": "Hello World"}

@app.get('/blog/{id}') ## this is a path parameter
def show(id: int): ## We can also specify the type of the path parameter
    return {"message": f"Blog post {id}"}

@app.get('/blog/{id}/comments')
def comments(id: int):
    #fetch comment with id=id
    return {"data": ["comment1", "comment2"]}

## Fast API always works serial wise, if two routes are same then it will firstly check
## the path coming first in the code.


## We can have a beautiful way of checking the API's
## by using Swagger UI at '/docs' route
