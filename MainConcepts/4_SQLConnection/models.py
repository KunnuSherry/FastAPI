from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    ## To create a relationship between two tables or models
    creator = relationship("User", back_populates="blogs")
    user_id = Column(Integer, ForeignKey('Users.id'))


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs  = relationship('Blog', back_populates='creator')