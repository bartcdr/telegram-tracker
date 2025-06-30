# MessageHandler.py
from telethon.tl.types import Message
from typing import Any
from pathlib import Path
from ChatHTMLManager import ChatHTMLManager


def find_chats_html() -> Path:
    """Ищет файл chats.html по шаблону DataExport*/list/chats.html."""
    matches = list(Path(".").glob("DataExport*/lists/chats.html"))
    if not matches:
        raise FileNotFoundError("Файл chats.html не найден по шаблону DataExport*/lists/chats.html")
    return matches[0]


class MessageHandler:
    """Класс для обработки входящих сообщений."""

    chat_manager = ChatHTMLManager(find_chats_html())

    @staticmethod
    async def handleMessage(event: Any) -> None:
        """Обрабатывает входящее сообщение и выводит его в терминал.

        Args:
            event (Any): Событие сообщения от Telethon.
        """
        message: Message = event.message

        sender = await event.get_sender()
        if sender:
            first_name = getattr(sender, "first_name", "")
            last_name = getattr(sender, "last_name", "")
            username = getattr(sender, "username", "")
            sender_id = getattr(sender, "id", None)

            display_name = f"{first_name} {last_name}".strip() or "Unknown"
            sender_name = display_name
            if username:
                sender_name += f" (@{username})"

            # Добавляем пользователя в HTML
            try:
                initial = display_name[0].upper()
                href = f"../chats/chat_{sender_id}/messages.html#allow_back"
                MessageHandler.chat_manager.add_user(
                    name=display_name,
                    initial=initial,
                    href=href,
                    messages_count=0
                )
            except Exception as e:
                print(f"[HTML Sync Error]: {e}")
        else:
            sender_name = "Unknown Sender"

        # Выводим сообщение в терминал
        if message.text:
            print(f"From {sender_name}: {message.text}")
        else:
            print(f"From {sender_name}: Received a non-text message (e.g., media, sticker)")