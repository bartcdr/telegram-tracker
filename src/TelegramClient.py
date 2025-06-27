# Класс для управления Telegram-клиентом.
from telethon import events

from telethon import TelegramClient
from typing import Callable

class TelegramClientManager:
    """Класс для управления Telegram клиентом."""

    def __init__(self, apiId: int, apiHash: str, sessionName: str):
        """Инициализация клиента.

        Args:
            apiId (int): Telegram API ID.
            apiHash (str): Telegram API Hash.
            sessionName (str): Имя сессии для сохранения авторизации.
        """
        self.client = TelegramClient(sessionName, apiId, apiHash)

    async def start(self) -> None:
        """Запускает клиент и выполняет авторизацию через терминал."""
        try:
            await self.client.start()
            print("Клиент запущен. Ожидаем сообщения...")
        except Exception as e:
            print(f"Ошибка при запуске клиента: {e}")
            raise

    def registerMessageHandler(self, handler: Callable) -> None:
        """Регистрирует обработчик сообщений.

        Args:
            handler (Callable): Функция обработки сообщений.
        """
        self.client.on(events.NewMessage)(handler)

    async def run(self) -> None:
        """Запускает клиент в режиме ожидания сообщений."""
        try:
            await self.client.run_until_disconnected()
        except Exception as e:
            print(f"Ошибка при работе клиента: {e}")
            raise