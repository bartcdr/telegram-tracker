# MessageHandler.py
# Класс для обработки сообщений.

from telethon.tl.types import Message
from typing import Any

class MessageHandler:
    """Класс для обработки входящих сообщений."""

    @staticmethod
    async def handleMessage(event: Any) -> None:
        """Обрабатывает входящее сообщение и выводит его в терминал.

        Args:
            event (Any): Событие сообщения от Telethon.
        """
        message: Message = event.message
        if message.text:
            print(f"Text message: {message.text}")
        else:
            print("Received a non-text message (e.g., media, sticker)")