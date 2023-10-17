from pydantic import BaseModel
from typing import Union
import uuid


class ORM(BaseModel):
    class Config:
        orm_mode = True


class User(ORM):
    username: str


class UserCreate(User):
    hashed_password: str


class UserInfo(User):
    is_active: bool 


class UserInDB(User):
    id: int
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: Union[str, None] = None
