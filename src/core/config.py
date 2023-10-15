import os
from logging import config as logging_config
from core.logger import LOGGING
from pydantic import BaseSettings, PostgresDsn, Field


logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    project_name: str = "project_name"
    project_host: str = ...
    project_port: int = ...
    secret_key: str
    algorithm: str
    base_dir: str = Field(BASE_DIR, env="BASE_DIR")
    access_token_expire_minutes: int
    echo: bool = True
    local_redis_url: str
    redis_url: str
    redis_host: str
    redis_port: int
    static_url: str
    files_folder_path: str = Field(
        os.path.join(
            BASE_DIR,
            "files"
        ),
        env="FILES_BASE_DIR"
    )
    compression_types: list = Field(
        ["zip", "7z", "tar"],
        env="COMPRESSION_TYPES"
    )
    app_title: str
    database_dsn: PostgresDsn

    class Config:
        env_file = os.path.dirname(BASE_DIR) + "/.env"


app_settings = AppSettings()


