import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    bot_token: str
    admin_id: int
    media_path: Path = Path("welcome.jpg")
    db_path: str = "users.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
    logging.info("Configuration file loaded successfully.")
except Exception as e:
    logging.error(f"Configuration file loading error: {e}")
    exit(1)
