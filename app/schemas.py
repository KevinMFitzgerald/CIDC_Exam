from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

class AuthorCreate(BaseModel):
    id:int
    name:str
    email:str
    year_started:int

class AuthorRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    name:str
    email:str
    year_started:int

class BookCreate(BaseModel):
    Authorid:int
    title:str
    id:int
    pages:int

class BookCreateForAuthor(BaseModel):
    title:str

class BookRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    title:str
    Authorid=int


    
    