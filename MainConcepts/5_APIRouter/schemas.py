from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True

##############################################################
#For User
class User(BaseModel):
    name:str
    email: str
    password: str


class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List[Blog] = []
    class Config():
        orm_mode = True


## Response Model
class ShowBlog(BaseModel):
    title:str
    creator : ShowUser
    class Config():
        orm_mode = True

