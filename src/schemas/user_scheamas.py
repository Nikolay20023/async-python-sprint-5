from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    is_active: bool


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
