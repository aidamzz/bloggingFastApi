from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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

    comments = relationship("Comment", back_populates="post")

# SQLAlchemy model for comments
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author = Column(String(100))
    text = Column(Text)
    created_at = Column(TIMESTAMP)

    post = relationship("Post", back_populates="comments")

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Routes to interact with the database
@app.get("/posts/{post_id}")
def read_post(post_id: int):
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts/")
def create_post(title: str, content: str):
    db = SessionLocal()
    new_post = Post(title=title, content=content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

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

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
