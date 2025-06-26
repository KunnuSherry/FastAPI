from fastapi import FastAPI

app = FastAPI()

@app.get('/') ## This is a decorator also called Path
def index(): ## This is a function operation function. This may or may not be unique name
    return {"message": "Hello World"}

@app.get('/about')
def about():
    return {"message": "About Page"}