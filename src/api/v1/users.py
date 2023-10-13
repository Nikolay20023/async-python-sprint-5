from datetime import datetime, timedelta
from typing import Union, Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError

from schemas.users import UserCreate, UserInfo, Token, TokenData
from db.db import get_session
from services.entity import users_crud
from api.v1.utils import verify_password, get_password
from core.config import app_settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router_user = APIRouter()


@router_user.post("/register", status_code=status.HTTP_201_CREATED)
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
    return {
        "username": user_db.username,
        "is_active": user_db.is_active
    }
    

async def authenticate_user(
    password: str,
    username: str,
    db: AsyncSession = Depends(get_session),
):
    try:
        user = await users_crud.get(db=db, username=username)
    except:
        raise Exception
    if not verify_password(password, user.hashed_password):
        return {
            "data": "Пароль неверный"
        }
    return user


async def create_access_token(
    data: dict,
    expire_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, app_settings.secret_key, algorithm=app_settings.algorithm)
    return encode_jwt


async def get_current_user(
        token: Annotated[str, Depends(oath2_scheme)],
        db: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, app_settings.secret_key, algorithms=[app_settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await users_crud.get(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
        


@router_user.post("/auth", response_model=Token)
async def user_auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(
        minutes=app_settings.access_token_expire_minutes
    )
    access_token = await create_access_token(
        data={"sub": user.username},
        expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router_user.get("/me", response_model=UserInfo)
async def get_me(
    current_user: Annotated[UserInfo, Depends(get_current_user)]
):
    return current_user