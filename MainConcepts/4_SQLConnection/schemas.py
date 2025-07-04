from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str


## Response Model
class ShowBlog(BaseModel):
    title:str
    class Config():
        orm_mode = True



##############################################################
#For User
class User(BaseModel):
    name:str
    email: str
    password: str
