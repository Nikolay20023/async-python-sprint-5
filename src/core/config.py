import os
import redis
from logging import config as logging_config
from pydantic import BaseSettings, PostgresDsn, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    project_name: str = "project_name"
    project_host: str = ...
    project_port: int = ...

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    echo: bool = True
    
    cache_host: str
    cache_port: int

    file_folder = "files_storage"

    app_title: str
    database_dsn: PostgresDsn

    class Config:
        env_file = ".env"


app_settings = AppSettings()
mem_cache = redis.asyncio.Redis(host=app_settings.cache_host, port=app_settings.cache_port)

