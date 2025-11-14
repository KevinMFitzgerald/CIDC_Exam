# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import AuthorDB, Base,book
from app.schemas import (
    AuthorCreate,
    AuthorRead,
    BookCreateForAuthor,
    BookCreate,
    BookCreateForAuthor,
    BookRead
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def commit_or_rollback(db:Session,msg:str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail=msg)

# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("api/authors",response_model=AuthorRead,status_code=status.HTTP_201_CREATED)
def create_author(payload:AuthorCreate,db:Session=Depends(get_db)):
    author=AuthorDB(**payload.model_dump())
    db.add(author)
    commit_or_rollback(db,"author already exists")
    db.refresh(author)
    return author

@app.get("/api/authors",response_model=list[AuthorRead])
def list_author(db:Session=Depends(get_db)):
    stmt=select(AuthorDB).order_by(AuthorDB.id)
    return db.execute(stmt).scalar().all()

@app.get("/api/authors/{authors_id}",response_model=AuthorRead)
def get_author(author_id:int,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="author not found")
    return author

@app.put("/api/author/{author_id}",response_model=AuthorRead)
def update_author(author_id:int,payload:AuthorCreate,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="author not found")
    author.name=payload.name
    author.email=payload.email
    commit_or_rollback(db,"author update failed")
    db.refresh(author)
    return author

@app.delete("/api/author/{author_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id:int,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="author not found")
    db.delete(author)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/api/author/{author_id}",response_model=AuthorRead)
def update_author(author_id:int,payload:AuthorCreate,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="author not found")
    author.name=payload.name
    author.email=payload.email
    commit_or_rollback(db,"author update failed")
    db.refresh(author)
    return author

@app.post("api/book",response_model=BookRead,status_code=status.HTTP_201_CREATED)
def create_author(payload:BookCreate,db:Session=Depends(get_db)):
    author=book(**payload.model_dump())
    db.add(author)
    commit_or_rollback(db,"author already exists")
    db.refresh(author)
    return author
@app.get("/api/books",response_model=list[BookRead])
def list_book(db:Session=Depends(get_db)):
    stmt=select(book).order_by(book.id)
    return db.execute(stmt).scalar().all()

@app.get("/api/books/{id}",response_model=BookRead)
def get_book(id:int,db:Session=Depends(get_db)):
    book=db.get(book,id)
    if not book:
        raise HTTPException(status_code=404,detail="author not found")
    return book


