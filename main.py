from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI()

# Database connection settings
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/db_name"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# SQLAlchemy model for posts
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    created_at = Column(TIMESTAMP)
    author = Column(String(100))
    tags = Column(String(255))

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

# SQLAlchemy model for comments
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author = Column(String(100))
    text = Column(Text)
    created_at = Column(TIMESTAMP)

    post = relationship("Post", back_populates="comments")

# SQLAlchemy model for users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Secret key to sign JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authenticate user
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the current user from the token
async def get_current_user(token: str = Depends(get_token), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Dependency to get the current database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Routes for user authentication
@app.post("/register/")
def register_user(username: str, email: str, password: str, db = Depends(get_db)):
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "email": db_user.email}

@app.post("/login/")
def login_user(username: str, password: str, db = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Routes to interact with the database
@app.post("/posts/", dependencies=[Depends(get_current_user)])
def create_post(title: str, content: str, author: str, tags: str = None, db = Depends(get_db)):
    new_post = Post(title=title, content=content, author=author, tags=tags)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/", dependencies=[Depends(get_current_user)])
def read_posts(filter_date: str = None, author: str = None, tags: str = None, db = Depends(get_db)):
    query = db.query(Post)
    if filter_date:
        query = query.filter(Post.created_at == filter_date)
    if author:
        query = query.filter(Post.author == author)
    if tags:
        query = query.filter(Post.tags.contains(tags))
    return query.all()
    
@app.post("/posts/")
def create_post(title: str, content: str, author: str, tags: str = None):
    db = SessionLocal()
    new_post = Post(title=title, content=content, author=author, tags=tags)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/")
def read_posts(filter_date: str = None, author: str = None, tags: str = None):
    db = SessionLocal()
    query = db.query(Post)
    if filter_date:
        query = query.filter(Post.created_at == filter_date)
    if author:
        query = query.filter(Post.author == author)
    if tags:
        query = query.filter(Post.tags.contains(tags))
    return query.all()

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str, content: str, author: str, tags: str = None):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    post.author = author
    post.tags = tags
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.post("/posts/{post_id}/comments/")
def create_comment(post_id: int, author: str, text: str):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(post_id=post_id, author=author, text=text)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@app.get("/posts/{post_id}/comments/")
def read_comments(post_id: int):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.comments

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    db = SessionLocal()
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

# Implement other CRUD operations for posts and comments similarly...

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
