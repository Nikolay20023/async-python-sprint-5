from models import User, File
from schemas.users import UserCreate
from services.users import UserDB
from services.files import FileDB
from schemas.files import FileCreater


class UsersEntity(UserDB[User, UserCreate]):
    pass


class FilesEntity(FileDB[File, FileCreater]):
    pass


users_crud = UsersEntity(User)
files_crud = FilesEntity(File)
