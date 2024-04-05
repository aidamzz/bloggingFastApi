from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import models  
from .database import engine, SessionLocal
from .api import posts as posts_api
models.Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

app = FastAPI()

app.include_router(posts_api.router, prefix="/posts", tags=["posts"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
