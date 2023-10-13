from datetime import datetime, timedelta
from typing import Union, Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError

from schemas.users import UserCreate, UserInfo, Token
from db.db import get_session
from services.entity import users_crud
from api.v1.utils import verify_password, get_password


oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router_user = APIRouter()


@router_user.post("/register",)
async def user_registration(
    obj_data: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    if not obj_data:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    obj_data.hashed_password = get_password(obj_data.hashed_password)

    try:
        user_db = await users_crud.create(db, obj_in=obj_data)
    except IntegrityError:
        return {
            "data": "username уже занет"
        }
    finally:
        return Response(UserInfo(**user_db.__dict__), status_code=status.HTTP_201_CREATED)


@router_user.post("/auth", response_model=Token)
async def user_auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
):
    pass