import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def generate_uuid():
    return str(uuid.uuid4())  # Generate a UUID and convert it to a string

class Post(Base):
    __tablename__ = "posts"
    id = Column(String(36), primary_key=True, index=True, default=generate_uuid)
    title = Column(String(255), index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())
    author_id = Column(String(36), ForeignKey('users.id'))
    tags = Column(String(255))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(String(36), primary_key=True, index=True, default=generate_uuid)
    post_id = Column(String(36), ForeignKey("posts.id"))
    author_id = Column(String(36), ForeignKey('users.id'))
    text = Column(Text)
    created_at = Column(TIMESTAMP)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, index=True, default=generate_uuid)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
