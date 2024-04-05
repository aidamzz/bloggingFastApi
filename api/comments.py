from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database  # Adjust import paths as needed

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts/{post_id}/comments/", response_model=schemas.Comment)
def create_comment_for_post(post_id: str, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    # Verify post exists
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = models.Comment(**comment.dict(), post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/posts/{post_id}/comments/", response_model=List[schemas.Comment])
def get_comments_for_post(post_id: str, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: str, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(db_comment)
    db.commit()
    return db_comment
