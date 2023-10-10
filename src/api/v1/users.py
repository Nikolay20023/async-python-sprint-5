from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def get_password(password):
    return pwd_context.hash(password)


@router.post("/register")
async def user_registration():
    pass


@router.post("/auth")
async def 