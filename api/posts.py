from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import models, schemas
from ..database import SessionLocal
from fastapi.responses import JSONResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, author_id: Optional[str] = None, 
               date: Optional[datetime] = None, tags: Optional[str] = None, 
               db: Session = Depends(get_db)):
    query = db.query(models.Post)
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    if date:
        query = query.filter(models.Post.created_at == date)
    if tags:
        query = query.filter(models.Post.tags.contains(tags))
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: str, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for var, value in vars(post_update).items():
        setattr(post, var, value) if value else None
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Post successfully deleted"})