import os
from logging import config as logging_config
from core.logger import LOGGING
from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    project_name: str = "project_name"
    project_host: str = ...
    project_port: int = ...
    echo: bool = True
    app_title: str
    database_dsn: PostgresDsn

    class Config:
        env_file = ".env"


app_settings = AppSettings()

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
