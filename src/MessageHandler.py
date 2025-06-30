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

        # Получаем информацию об отправителе
        sender = await event.get_sender()
        if sender:
            first_name = getattr(sender, "first_name", "")
            last_name = getattr(sender, "last_name", "")
            username = getattr(sender, "username", "")

            # Формируем строку имени
            sender_name = f"{first_name} {last_name}".strip()
            if username:
                sender_name += f" (@{username})"
        else:
            sender_name = "Unknown Sender"

        # Выводим сообщение в терминал
        if message.text:
            print(f"From {sender_name}: {message.text}")
        else:
            print(f"From {sender_name}: Received a non-text message (e.g., media, sticker)")