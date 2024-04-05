from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import models  
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example route to demonstrate use of the database session
@app.get("/posts/")
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
