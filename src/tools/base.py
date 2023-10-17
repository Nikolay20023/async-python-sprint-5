from core.config import app_settings


def join_user(id_: int, name: str):
    return ''.join([str(id), '_', name])