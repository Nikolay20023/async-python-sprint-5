from models import User
from schemas.users import UserCreate
from services.users import UserDB


class UsersEntity(UserDB[User, UserCreate]):
    pass


users_crud = UsersEntity(User)