from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def get_password(password):
    return pwd_context.hash(password)