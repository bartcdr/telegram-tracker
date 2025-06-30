# Config.py
# Чтение конфигурации из .env

from typing import Optional
from dotenv import load_dotenv
import os


class Config:
    """Класс для загрузки и валидации конфигурации из .env файла."""

    def __init__(self, env_path: str = "configuration.env"):
        """Инициализация конфигурации.

        Args:
            env_path (str): Путь к .env файлу.
        """
        load_dotenv(dotenv_path=env_path)
        self.api_id: Optional[int] = None
        self.api_hash: Optional[str] = None
        self.session_name: Optional[str] = None
        self._load_config()

    def _load_config(self) -> None:
        """Загружает конфигурацию из .env и проверяет её."""
        self.api_id = os.getenv("API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.session_name = os.getenv("SESSION_NAME") or "default_session"

        if not self.api_id:
            raise RuntimeError("❌ Не найден API_ID в configuration.env")
        if not self.api_hash:
            raise RuntimeError("❌ Не найден API_HASH в configuration.env")

    def getConfig(self) -> tuple[int, str, str]:
        """Возвращает конфигурационные данные.

        Returns:
            tuple[int, str, str]: API ID, API Hash, имя сессии.
        """
        return self.api_id, self.api_hash, self.session_name