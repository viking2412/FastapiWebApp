from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6)]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    text: str

class PostResponse(BaseModel):
    post_id: int
    text: str
    user_id: int
