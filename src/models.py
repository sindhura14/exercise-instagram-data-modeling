import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("user_from_id", Integer, ForeignKey('user.id')),
    Column("user_to_id", Integer, ForeignKey('user.id')),
)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username=Column(String(64),primary_key=True)
    firstname=Column(String(64),nullable=False)
    lastname=Column(String(64),nullable=False)
    email = Column(String(250), nullable=False)
    followers = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=(id == user_to_user.c.user_from_id),
        secondaryjoin=(id == user_to_user.c.user_to_id),
        userlist=True,
    )
    posts=relationship("Post", back_populates="user", uselist=True)
    comments=relationship("User", back_populates="user", uselist=False)

class Follower(Base):
    __tablename__ = "follower"
    user_from_id=Column(Integer, ForeignKey("user.id"), nullable=False)
    user_to_id=Column(Integer, ForeignKey("user.id"), nullable=False)

class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("user.id"), nullable=False)
    user=relationship("User", back_populates="posts", uselist=False)
    comments = relationship('Comment',back_populates="posts",uselist=False)

    

class Comment(Base):
    __tablename__ ='comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(64))
    author_id=Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id=Column(Integer, ForeignKey("post.id"), nullable=False)
    user=relationship("User", back_populates="comments", uselist=False)
    posts = relationship("Post", back_populates="comments", uselist=True)

class Media(Base):
    __tablename__ ='media'
    id = Column(Integer, primary_key=True)
    url = Column(String(128),nullable=False)
    post_id=Column(Integer, ForeignKey("post.id"), nullable=False)



    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
