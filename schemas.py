from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Example Pydantic model for creating a new post
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: str  
    tags: Optional[str] = None

# Example Pydantic model for updating an existing post
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    author_id: Optional[str] = None 

# Example Pydantic model for response schema
class Post(BaseModel):
    id: str  
    title: str
    content: str
    created_at: Optional[datetime] = None
    author_id: str
    tags: Optional[str] = None
# Schema for request body of new comment
class CommentCreate(BaseModel):
    text: str
    author_id: str  # Adjust based on how you identify users
    # post_id: str

# Schema for response body of comment
class Comment(BaseModel):
    id: str
    text: str
    author_id: str
    post_id: str
    created_at: Optional[datetime] = None
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: str
    username: str
    email: str
    class Config:
        orm_mode = True
class TokenData(BaseModel):
    username: Optional[str] = None